from django.shortcuts import render
from . import forms
from . import models
import json
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib import messages
from datetime import *
import decimal
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import sys
import os
from expensewebsite.settings import BASE_DIR
from decimal import Decimal
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
from rest_framework.decorators import api_view,throttle_classes
from expensewebsite import throttle
# Create your views here.




def create_notification(group,user='',admin_involved='',request_accepted=False,request_denied=False,admin_status_change=False):
    #groups=models.Custom_groups.objects.get(group_name=group)
    users=models.Members.objects.filter(group=group)
    for member in users:
        notification=models.Group_notification.objects.create(user_notification_for=member.member,group=group)
        if user!='':
            notification.user_involved=user
        if admin_involved!='':
            notification.admin_involved=admin_involved
        if request_accepted == True:
            notification.request_accepted=True
        if request_denied == True:
            notification.request_denied=True
        if admin_status_change == True:
            notification.admin_status_change=True
        notification.save()

def get_group_details(request,group):
    context={}
    context['group']=group
    context['members_detail']=[]
    is_member=False
    group_summary = list(models.Group_summary.objects.filter(group_name=group).values())
    for data in group_summary:
        if data['member_name_id']!=request.user.pk:
            data['member_name']=User.objects.get(pk=data['member_name_id'])
            context['members_detail'].append(data)
        else:
            is_member=True
            data['member_name']=User.objects.get(pk=data['member_name_id'])
            context['members_detail'].insert(0,data)
    context['is_member']=is_member        
    paginator=Paginator(context['members_detail'],5)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)        
    """ print(context['members_detail'])
    print(context['group']) """
    context['page_obj']=page_obj
    context['length']=len(context['members_detail'])
    return render(request,'groups/group_details.html',context)

def check_member(group , user):
    is_member_request=0
    try:
        is_member_request=models.Members.objects.get(group=group,member=user)
        return [is_member_request,True]
    except Exception as ex:
        return [is_member_request,False] 


def have_permission(group,user):
    permission=0
    try:
        permission=models.PermissionToVisit.objects.get(user=user,group=group)
        return [permission,True]
    except Exception as ex:
        return [permission,False]
    
def is_admin(user,group):
     return models.Admins.objects.filter(user=user,group=group).exists()

@login_required(login_url='/authentication/login')
def create_group(request):
    if request.method=='GET':
        form=forms.Create_group()
        context={'form':form}
        return render(request,'groups/create_group.html',context)
    else:
        form=forms.Create_group(request.POST)
        if form.is_valid():
            user=request.user
            data=form.cleaned_data
            group_name=data['group_name']
            group_password=data['group_password']
            group=models.Custom_groups.objects.create(group_name=group_name,group_password=group_password) 
            models.Admins.objects.create(user=user,group=group)
            #group=models.Custom_groups.objects.get(group_name=group_name)
            models.Members.objects.create(group=group,member=user)
            models.Group_summary.objects.create(group_name=group,member_name=user,member_total_contribution=0)
            models.Group_currency.objects.create(group=group)       
        else:
            print(form.is_valid()) 
        return redirect('create_group')


@login_required(login_url='/authentication/login')
def add_member(request,group):
    user=request.user

    if request.method=='GET':
        return render(request,'groups/add_member.html',{'group':group})
    else:
        if is_admin(user,group):
            member=models.User.objects.get(username=request.POST['member'])
            group=models.Custom_groups.objects.get(group_name=group)
            #print(989)
            models.PermissionToVisit.objects.create(user=member,permission_for_group=group)
            #print(987)
            models.Inbox.objects.create(user=member,group=group)
            return redirect('list_groups')
        else:    
            messages.error(request,'sorry either user is already a member or you are not the admin of this group')
            return redirect('add_member',group)


@login_required(login_url='/authentication/login')
def accept_request_user(request,group):
        try:
            inbox_message=models.Inbox.objects.get(user=request.user,group=group)
            inbox_message.delete()
            
            member=request.user
            group=models.Custom_groups.objects.get(group_name=group)
            models.Members.objects.create(member=member,group=group)
            models.Group_summary.objects.create(group_name=group,member_name=member,member_total_contribution=0)
            models.PermissionToVisit.objects.get(user=request.user,permission_for_group=group).delete()
            create_notification(group=group.group_name,user=request.user.username,request_accepted=True)
        except Exception as e:
            print(e)
            messages.warning(request,'something went wrong please try again')
            return redirect('expenses') 
        return redirect('list_groups')



@login_required(login_url='/authentication/login')
def deny_request_user(request,group):
    
    try:
        inbox_message=models.Inbox.objects.get(user=request.user,group=group)
        inbox_message.delete()
        models.PermissionToVisit.objects.get(user=request.user,permission_for_group=group).delete()
        create_notification(group=group,user=request.user.username,request_denied=True)
    except Exception as e:
        print(e)
        messages.warning(request,'something went wrong')
        return redirect('expenses')    
    
    return redirect('expenses')


@login_required(login_url='/authentication/login')
def list_groups(request):
    members = models.Members.objects.filter(member=request.user.pk)
    groups=[]
    
    for member in members:
        individual_group=models.Custom_groups.objects.get(group_name=member.group)
        data={}
        data['group_name']=individual_group.group_name
        try:
            admin=models.Admins.objects.get(user=request.user,group=individual_group)

            data['group_admin']=True
        except Exception as ex:
            data['group_admin']=False     
        
        groups.append(data)
        print(individual_group)
    paginator=Paginator(groups,5)
    page_num=request.GET.get('page')
    page_obj=paginator.get_page(page_num)
    context={
        'groups':groups,
        'page_obj':page_obj
    }
    return render(request,'groups/list_groups.html',context)


@login_required(login_url='/authentication/login')
def edit_group(request,group):
    """ admin=models.Custom_groups.objects.get(group_name=group)
    print(admin) """
    if not is_admin(request.user,group):
        messages.error(request,'unauthorized request')
        return redirect('expenses')
    members=models.Members.objects.filter(group=group)
    member=[]
    for memb in members:
        #print(memb.member)
        temp_dict={}
        temp_dict['member']=memb.member
        if not is_admin(memb.member,group):
            temp_dict['admin']=False
        else:
            temp_dict['admin']=True
        member.append(temp_dict)
        paginator=Paginator(member,4)
        page_number=request.GET.get('page')
        page_obj=paginator.get_page(page_number)
        context={}
        context['page_obj']=page_obj
    #print(member)
    return render(request,'groups/edit_group.html',{'page_obj':page_obj,'group':group})




@login_required(login_url='/authentication/login')
#remained to be updated with post request
def member_list(request):
    if request.method=='POST':
        searchText=json.loads(request.body)['searchText']
        member_list=[x['username'] for x in list(User.objects.filter(username__icontains=searchText).values())]
        #print(member_list)
        return JsonResponse(list(member_list),safe=False)



@login_required(login_url='/authentication/login')
def group_details(request,group):
    """ print(type(datetime.today().date))
    print(check_member(group,request.user)[1]) """
    #members=list(models.Members.objects.filter(group=group).values())
    if have_permission(group,request.user)[1]:
        return get_group_details(request,group)
    else:
        if check_member(group,request.user)[1]==True:
            return get_group_details(request,group)        
        else:
            messages.error(request,'unauthorized request')
            return redirect('expenses')
        


@login_required(login_url='/authentication/login')   
def group_individual_detail(request,group,pk):
    if check_member(group,request.user)[1]==True:
        expenses=models.Group_individual_expenses.objects.filter(group=group,individual_name=pk)
        paginator=Paginator(expenses,5)
        page_number=request.GET.get('page')
        page_obj=paginator.get_page(page_number)
        context={
            'group':group,
            'expenses':expenses,
            'page_obj':page_obj,
            'pk':pk
            }
        return render(request,'groups/group_individual_details.html',context)
        
    else: 
        messages.warning(request,'unauthorized access tried returned to home page')
        return redirect('expenses')   
    



@login_required(login_url='/authentication/login')
def add_group_individual_expense(request,group,pk):
    if pk!=request.user.pk:
        messages.warning(request,'unauthorized access tried returned to home page')
        return redirect('expenses') 
    if request.method=='GET':
        context={}
        context['group']=group
        context['pk']=pk
        """ print(group)
        print(int(datetime.today().day)) """
        return render(request,'groups/add_group_individual_expenses.html',context)
    else:
        data=request.POST
        expense_amount=data['expense_amount']
        expense_date=data['expense_date']
        description=data['description']
        individual_name=models.User.objects.get(pk=request.user.pk)
        #print(expense_date[0:4],expense_date[5:7],expense_date[8:10])
        group=models.Custom_groups.objects.get(group_name=group)
        models.Group_individual_expenses.objects.create(individual_name=individual_name,expense_amount=expense_amount,expense_date=expense_date,description=description,group=group)
        group_user=models.Group_summary.objects.get(group_name=group.pk,member_name=request.user)
        group_user.member_total_contribution+=decimal.Decimal(expense_amount)
        group_user.save()
        context={}
        context['group']=group
        expenses=models.Group_individual_expenses.objects.filter(group=group,individual_name=individual_name)
        #print(expenses.values())
        context['expenses']=expenses
        return redirect('group_individual_details',group,request.user.pk)
         




    #-----------------------------------------------



@login_required(login_url='/authentication/login')
def join_group(request):
    if request.method == 'GET':
        return render(request,'groups/join_group.html')
    else:
        print('here')
        searchText=json.loads(request.body)['searchText']
        groups=[x['group_name'] for x in list(models.Custom_groups.objects.filter(group_name__icontains=searchText).values())]
        return JsonResponse(groups,safe=False)
        


@login_required(login_url='/authentication/login')
def join_request(request):
    if request.method == 'POST':
        group=request.POST['group']
        group=models.Custom_groups.objects.get(group_name=group)
        models.Inbox.objects.create(user=request.user,group=group,sent=True)
    return redirect('expenses')


@login_required(login_url='/authentication/login')
def list_requests(request,group):
    if is_admin(request.user,group):
        requests=models.Inbox.objects.filter(group=group,sent=True).order_by('id')
        paginator=Paginator(requests,5)
        page_number=request.GET.get('page')
        page_obj=paginator.get_page(page_number)

        return render(request,'groups/join_requests.html',context={'page_obj':page_obj,'requests':requests,'group':group})
    else:
        messages.warning(request,'you are not a admin of this group')
        return render('expenses')


@login_required(login_url='/authentication/login')
def list_admins(request,group):
    if check_member(request.user,group)[1]:
        admins=models.Admins.objects.filter(group=group)
        paginator=Paginator(admins,5)
        page_number=request.GET.get('page')
        page_obj=paginator.get_page(page_number)
        context={}
        context['page_obj']=page_obj
        return render(request,'groups/list_admins.html',context)
    else:
        messages.error(request,'not a group member')
        return redirect('expenses')
    


@login_required(login_url='/authentication/login')
def change_admin_status(request,user,group):
    user=User.objects.get(username=user)
    group_name=group
    if is_admin(request.user,group):
        if is_admin(user,group):
            if models.Admins.objects.filter(group=group).count()>1:    
                models.Admins.objects.get(user=user,group=group).delete()
            else:
                messages.warning(request,'please add atleast one admin before deleting this user')
                return get_group_details(request,group)
        else:
            group=models.Custom_groups.objects.get(group_name=group)
            models.Admins.objects.create(user=user,group=group)
        
        create_notification(group=group_name,user=user.username,admin_involved=request.user.username,admin_status_change=True)
        return redirect('list_groups')
    else:
        messages.warning(request,'you are not authorized for this operation')
        return redirect('expenses')


@login_required(login_url='/authentication/login')
def accept_request_group(request,group,user):
    if is_admin(request.user,group):
        group=models.Custom_groups.objects.get(group_name=group)
        user=User.objects.get(username=user)
        models.Members.objects.create(group=group,member=user)
        models.Group_summary.objects.create(group_name=group,member_name=user,member_total_contribution=0)
        models.Inbox.objects.get(group=group,sent=True,user=user).delete()
        create_notification(group.group_name,user.username,admin_involved=request.user.username,request_accepted=True)
        return redirect('group_details',group)
    messages.error(request,'unauthorized access')
    return redirect('group_details',group)


@login_required(login_url='/authentication/login')
def deny_request_group(request,group,user):
    if is_admin(request.user,group):
        user=User.objects.get(username=user)
        models.Inbox.objects.get(group=group,sent=True,user=user).delete()
        create_notification(group,user.username,admin_involved=request.user.username,request_denied=True)
        models.Group_notification.objects.create(group=group,user_notification_for=user,user_involved=user.username,admin_involved=request.user,request_denied=True)
        return redirect('group_details',group)
    messages.error(request,'unauthorized access')
    return redirect('group_details',group)







#remained to be updated
@login_required(login_url='/authentication/login')
def change_currency(request,group):
    if is_admin(request.user,group):
        current_currency=models.Group_currency.objects.get(group=group).currency  
        if request.method=='GET' :
            file_path=os.path.join(BASE_DIR,'currencies.json')
            currencies_list=[]
            with open(file_path,'r') as json_file:
                data=json.load(json_file)
                for key,value in data.items():
                    currencies_list.append({'name':key,'value':value})
            return render(request,'groups/group_currency.html',{'currencies_list':currencies_list,'group':group,'current_currency':current_currency})
    else:
        messages.warning('you are not an admin of this group')
        return redirect('expesnses')

@api_view(['POST'])
@throttle_classes([throttle.automation_throttle])    
def currency_modify(request,group): 
    current_currency=models.Group_currency.objects.get(group=group).currency   
    if request.method=='POST':
        currency=request.POST['currency_list']
        #print(current_currency)
        if current_currency!=currency:
            options=webdriver.ChromeOptions()
            options.add_argument('--headless=new')
            driver =webdriver.Chrome(options=options)
            driver.get("https://www.google.com/search?q=free+currency+converter")
            elem = Select(driver.find_element(By.CLASS_NAME, "zuzy3c"))
            elem.select_by_visible_text(current_currency)
            time.sleep(0.5)
            input_element=driver.find_element(By.CLASS_NAME,"ZEB7Fb")
            input_element.clear()
            input_element.send_keys("100000")
            time.sleep(0.5)
            #value_of_previous_currency = driver.find_element(By.CLASS_NAME, "a61j6").get_attribute('value')
            elem1=Select(driver.find_element(By.CLASS_NAME,"NKvwhd"))
            elem1.select_by_visible_text(currency)
            time.sleep(0.5)
            value_of_new_currency=driver.find_element(By.CLASS_NAME, "a61j6").get_attribute('value')
            #print("value of previous currency =",value_of_previous_currency)
            #print("value of new currency = ",value_of_new_currency)
            driver.close()


            individual_expenses=models.Group_individual_expenses.objects.filter(group=group)
            for expense in individual_expenses:
                amount=(Decimal(expense.expense_amount)*Decimal(value_of_new_currency))/Decimal(100000)
                expense.expense_amount=round(amount)
                expense.save()
            
            group_summary=models.Group_summary.objects.filter(group_name=group)
            for summary in group_summary:
                amount=(Decimal(summary.member_total_contribution)*Decimal(value_of_new_currency))/Decimal(100000)
                summary.member_total_contribution=round(amount)
                summary.save()
            current_currency=models.Group_currency.objects.get(group=group)
            current_currency.currency=currency
            current_currency.save()
    return redirect('group_details',group)
            


@login_required(login_url='/authentication/login')
def group_summary_admin(request,group):
    return render(request,'groups/group_summary_admin.html',{'group':group})


@login_required(login_url='/authentication/login')
def group_summary_individual(request):
    return render(request,'groups/group_summary_individual.html')


@login_required(login_url='/authentication/login')
def group_stat_admin(request,group):
    if request.method=='POST':
        if is_admin(request.user,group):
            from_date=datetime.now()-timedelta(days=60)
            to_date=datetime.now()-timedelta(days=-1)
            data=models.Group_individual_expenses.objects.filter(group=group,expense_date__gte= from_date,expense_date__lt=to_date)
            context={}
            def get_name(data):
                return str(data.individual_name)
            distinct_names=list(set(map(get_name,data)))
            print(distinct_names)
            for name in distinct_names:
                context[name]=0
            
            for datum in data:
                context[str(datum.individual_name)]+=datum.expense_amount
            return JsonResponse({'group_summary':context},safe=False)
    


@login_required(login_url='/authentication/login')
def group_stat_individual(request):
    if request.method=='POST':
        from_date=datetime.now()-timedelta(days=60)
        to_date=datetime.now()-timedelta(days=-1)
        data=models.Group_individual_expenses.objects.filter(expense_date__gte=from_date,individual_name=request.user)
        dataset={}
        def get_group_name(data):
            return data.group.group_name
        unique_groups=list(set(map(get_group_name,data)))
        for group in unique_groups:
            dataset[group]=0
        for datum in data:
            dataset[datum.group.group_name]+=datum.expense_amount
        """ for datum in data:
            print(datum.individual_name,datum.expense_date,datum.expense_amount) """
        return JsonResponse({'dataset':dataset},safe=False)



## user exit and removal along with notification







@login_required(login_url='/authentication/login')  
def exit_group(request,group,user):
    print('user is ',type(user),'request.user is',type(request.user.username))
    if(request.user.username!=user):
        messages.warning(request,'You are not authorized to do this operation')
        return redirect('expenses')
    if request.method=='GET':
        context={'message':'do you really want to leave ' + str(group)}
        return render(request,'partials/confirm_deletion.html',context)
    else:
        
        user=User.objects.get(username=user)

        group=models.Custom_groups.objects.get(group_name=group)
        if models.Members.objects.filter(group=group).count()==1:  
            models.Custom_groups.objects.get(group_name=group.group_name).delete()
        else:
            if is_admin(user,group):
                    if models.Admins.objects.filter(group=group).count()>1:
                        models.Admins.objects.get(user=user,group=group).delete()
                    else:
                        messages.warning(request,'please add atleast one admin before leaving the group')
                        return redirect('edit_group',group)
                        return get_group_details(request,group)
        
            models.Members.objects.get(group=group,member=user).delete()
            if models.Group_individual_expenses.objects.filter(individual_name=user,group=group):
                models.Group_individual_expenses.objects.filter(individual_name=user,group=group).delete()
            models.Group_summary.objects.get(group_name=group,member_name=user).delete()
            create_notification(group.group_name,user.username)
    messages.success(request,'you have successfully exited the group '+str(group))
    return redirect('expenses')



@login_required(login_url='/authentication/login')
def remove_user(request,user,group):

    user=User.objects.get(username=user)
    if request.method=='GET':
        context={'message':'do you really want to remove '+str(user) + ' from ' + str(group)}
        return render(request,'partials/confirm_deletion.html',context)
    else:
        if is_admin(request.user,group):
            if models.Members.objects.filter(group=group).count() == 1:
                models.Custom_groups.objects.get(group_name=group).delete()
            else:
                if is_admin(user,group):
                    if models.Admins.objects.filter(group=group).count()>1:
                        models.Admins.objects.get(user=user,group=group).delete()
                    else:
                        messages.warning(request,'please add atleast one admin before deleting this user')
                        return get_group_details(request,group)

                models.Members.objects.get(member=user,group=group).delete()
                if models.Group_individual_expenses.objects.filter(individual_name=user,group=group):
                    models.Group_individual_expenses.objects.filter(individual_name=user,group=group).delete()
                models.Group_summary.objects.get(group_name=group,member_name=user).delete()
                #models.Custom_groups.objects.get(group=group)
                create_notification(user=user.username,group=group,admin_involved=request.user.username)
                models.Group_notification.objects.create(user_notification_for=user,user_involved=user.username,group=group,admin_involved=request.user.username)
                return redirect('group_details',group)
        else:
            messages.warning(request,'unauthorized access only admins are authorized for this operation')
        return redirect('expenses')


@login_required(login_url='/authentication/login')
def delete_group(request,group):
    if request.method=='GET':
        context={'message':'do you really want to delete group'+str(group)}
        return render(request,'partials/confirm_deletion.html',context)
    else:
        if is_admin(user=request.user,group=group):
            models.Custom_groups.objects.get(group_name=group).delete()
        else:
            messages.danger(request,'Unauthorized requests, only Admins can do this ')
        create_notification(group=models.Custom_groups.objects.get(group_name=group),admin_involved=request.user.username)
        return redirect('expenses')


@login_required(login_url='/authentication/login')
def get_notification(request):
    notification_exists=notifications=models.Group_notification.objects.filter(user_notification_for=request.user).exists()
    if request.method=='GET':
        notifications=''
        try:
            notifications=models.Group_notification.objects.filter(user_notification_for=request.user)
        except Exception as e:
            print(e)
            notification_exists=False
    
        return render(request,'groups/list_notification.html',{'notifications':notifications,'count':notification_exists })
    else:
        return JsonResponse({'notifications':notification_exists},safe=False)





@login_required(login_url='/authentication/login')
def delete_notifications(request,id):
    if models.Group_notification.objects.get(pk=id).user_notification_for != request.user:
        messages.error(request,'you are trying to delete someone else\'s notification ')
        return redirect('expenses')
    models.Group_notification.objects.get(pk=id).delete()
    return redirect('list_notification')




@login_required(login_url='/authentication/login')
def edit_group_expense(request,id):
    values=models.Group_individual_expenses.objects.get(pk=id)
    if(request.user.pk!=values.individual_name.pk):
        messages.error(request,'you are tyring  to edit some one else\'s data ')
        return redirect('expenses')
    if request.method=='GET':
        values.expense_date=values.expense_date.strftime("%Y-%m-%d")
        context={
            'values':values
        }
        return render(request,'groups/edit_group_expenses.html',context)
    else:
        post_data=request.POST
        values.expense_amount=post_data['expense']
        values.expense_date=post_data['date']
        values.description=post_data['description']
        values.save()
        group_user=models.Group_summary.objects.get(group_name=values.group,member_name=request.user)
        update_by=decimal.Decimal(post_data['expense'] )- decimal.Decimal(post_data['previous_value'])
        group_user.member_total_contribution+=update_by
        group_user.save()
        messages.success(request,'succesfully updated')
    return redirect('group_individual_details',values.group.group_name,values.individual_name.pk)



@login_required(login_url='/authentication/login')
def delete_individual_expense(request,id):
    if request.method=='GET':
        
        context={
            'message':'do you really want to delete this expense'
            }
        return render(request,'partials/confirm_deletion.html',context)
    else:
        values=models.Group_individual_expenses.objects.get(pk=id)
        if(values.individual_name.pk!=request.user.pk):
            messages.warning(request,'please Be ethical and don\'t access what is not yours ')
            return redirect('expenses')
        group_user=models.Group_summary.objects.get(group_name=values.group,member_name=request.user)
        update_by=values.expense_amount
        group_user.member_total_contribution-=update_by
        group_user.save()
        values.delete()
        messages.success(request,'your expense is successfully deleted')
        return redirect('group_individual_details',values.group.group_name,values.individual_name.pk)



@login_required(login_url='/authentication/login')
def custom_404(request,exception):
    return render(request,'partials/404.html')


@login_required(login_url='/authentication/login')
def custom_500(request):
    return render(request,'partials/404.html')


#search groups
@login_required(login_url='/authentication/login')
def search_groups(request):
    if request.method=='POST':
        search_str=json.loads(request.body).get('searchText')
        group_list=models.Custom_groups.objects.filter(group_name__icontains=search_str)
        groups=[]
        for group in group_list:
            if models.Members.objects.filter(group=group,member=request.user).exists():
                groups.append({'group_name':group.group_name,'is_admin':False,'user':request.user.username})
            if is_admin(user=request.user,group=group):
                groups[-1]['is_admin']=True
        #groups=models.Members.objects.filter(group.group_name__icontains=search_str,member=request.user)
        return JsonResponse(groups,safe=False)
    
@login_required(login_url='/authentication/login')    
def search_members(request,group):
    if(request.method=='POST'):
        group=models.Custom_groups.objects.get(group_name=group)
        search_str=json.loads(request.body).get('searchText')
        users=User.objects.filter(username__contains=search_str)
        members=[]
        for user in users:
            if models.Members.objects.filter(member=user,group=group).exists():
                members.append( {'member':user.username,'is_admin':False,'group':group.group_name})
            if is_admin(user,group=group):
                members[-1]['is_admin']=True
    return JsonResponse(members,safe=False)

@login_required(login_url='/authentication/login') 
def search_group_individual_expenses(request,group,pk):
    if(request.method=='POST'):
        search_str=json.loads(request.body).get('SearchText')
        expenses=models.Group_individual_expenses.objects.filter(
            group=group,individual_name=pk,expense_date__icontains=search_str)|models.Group_individual_expenses.objects.filter(
                group=group,individual_name=pk,expense_amount__istartswith=search_str)|models.Group_individual_expenses.objects.filter(
                        group=group,individual_name=pk,description__icontains=search_str)
        expenses=list(expenses.values())
        expenses.append({'request_user':request.user.pk})
        return JsonResponse(expenses,safe=False)

