from django.shortcuts import render,redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.urls import reverse
from .utils import token_generator
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import datetime

from django.utils.encoding import force_bytes,DjangoUnicodeDecodeError,force_str
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site

from django.contrib import auth 
# Create your views here.

class UserNameValidationView(View):
    def post(self,request):
        data=json.loads(request.body)
        username=data['username']

        if not str(username).isalnum():
            return JsonResponse( {'username_error':'username should only contain alpha numeric character' }
            ,status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'sorry username is used,chose another one'},status=409)
        return JsonResponse({'username_valid':True})


class EmailValidationView(View):
    def post(self,request):
        data=json.loads(request.body)
        email=data['email']

        if not validate_email(email):
            return JsonResponse( {'email_error':'email is invalid' },status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error':'sorry email is used,chose another one'},status=409)
        return JsonResponse({'email_valid':True})



class RegistrationView(View):
    def get(self,request):
        return render(request,'authentication/register.html')
    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        
        context={'fieldvalues':request.POST}

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password)<6:
                    messages.error(request,'password too short')
                    return render(request,'authentication/register.html',context=context)

                user=User.objects.create_user(username=username,email=email)
                user.set_password(password)
                user.save()
                #user.is_active=False

                uidb64=urlsafe_base64_encode(force_bytes(user.pk))

                domain=get_current_site(request).domain
                
                link=reverse('activate',kwargs={'uidb64':uidb64,'token':token_generator.make_token(user)})

                activate_url='http://'+domain+link
                email_subject='activate your account'
                email_body='hi '+user.username+' please use this link to verify your account\n '+ activate_url
                send_email=EmailMessage(
                    email_subject,
                    email_body,
                    'noreply@semycolon.com',
                    [email],

                )
                print(user.is_active)
                #send_email.send(fail_silently=False)
                messages.success(request,'account successfully created')
                return redirect('login')
        return render(request,'authentication/register.html')


class verificationView(View):
    def get(self,request,uidb64,token):
        try:
            id=force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)
            if not token_generator.check_token(user,token):
                #print(user.is_active)
                messages.error(request,'user already activated')
                return redirect('login')
            if not user.is_active:
                print('not active')
                return redirect('login')
            user.is_active=True
            user.save()
            messages.success(request,'account activated successfully')
            return redirect('login')
        except Exception as ex:
            pass
        print('normal')
        return redirect('login')


class LoginView(View):
    def get(self,request):
        return render(request,'authentication/login.html')
    def post(self,request):
        username=request.POST['username']
        password=request.POST['password']
        print(password+username)
        if username and password:

            user=auth.authenticate(username=username,password=password)
            print(user)
            if user is not None:
                if user.is_active:
                    auth.login(request,user)
                    messages.success(request,'welcome '+ user.username + 'you are logged in')
                    return redirect('expenses')
                messages.error(request,'your account is not activated please check your email')
                return render(request,'authenticate/login.html')
            messages.error(request,'invalid credintials try again')
            return render(request,'authentication/login.html')
        messages.error(request,'please fill both the fields')
        return render(request,'authentication/login.html')


class logoutView(View):
    def post(self,request):
        auth.logout(request)
        messages.success(request,'you have been logged out')
        return redirect('login')
    

class RequestPasswordResetEmail(View):
    def get(self,request):
        return render(request,'authentication/reset-password.html')
    def post(self,request):
        email=request.POST.get('email')
        context={
            'values':request.POST
        }
        if not validate_email(email):
            messages.error(request,'please enter a valid email address')
            return render(request,'authentication/reset-password.html',context)
        
        user = User.objects.filter(email=email)
        print(len(user))
        if len(user) < 1:
            messages.success(request,'we have a sent you a password reset link on your registered email')
            return redirect('login')
        print(user[0].username)
        uidb64=urlsafe_base64_encode(force_bytes(user[0].pk))

        domain=get_current_site(request).domain
        
        link=reverse('password-reset',kwargs={'uidb64':uidb64,'token':PasswordResetTokenGenerator().make_token(user[0])})

        reset_url='http://'+domain+link
        email_subject='reset your password'
        email_body='hi there, please use this link to reset your password\n '+ reset_url
        send_email=EmailMessage(
            email_subject,
            email_body,
            'noreply@semycolon.com',
            [email],

        )
        send_email.send(fail_silently=False)
        messages.success(request,'email sent successfully')
        return redirect('login')


class completePasswordReset(View):
    def get(self,request,uidb64,token):
        context={
            'uidb64':uidb64,
            'token':token
        }
        try:
            pk=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=pk)
            if not PasswordResetTokenGenerator().check_token(user,token):
                messages.error(request,'password link is invalid please generate a new one')
                return render(request,'authentication/reset-password.html')  
        except Exception as id:
            print(id)
            messages.error(request,'something went wrong'+id)
            return render(request,'authentication/set-new-password.html',context)   
            

        return render(request,'authentication/set-new-password.html',context)
    def post(self,request,uidb64,token):
        context={
            'uidb64':uidb64,
            'token':token
        }
        password=request.POST['password']
        password2=request.POST['password2']
        if password!=password2:
            messages.warning(request,'passwords don not match')
            return render(request,'authentication/set-new-password.html',context)
        if len(password)<6:
            messages.warning(request,'password too shorts')
            return render(request,'authentication/set-new-password.html',context)
        try:
            pk=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=pk)
            user.set_password(password)
            user.save()
            messages.success(request,'password reset successfully, login with your new password')
            return redirect('login')    
        except Exception as id:
            messages.error(request,'something went wrong')
            return render(request,'authentication/set-new-password.html',context)   
            




