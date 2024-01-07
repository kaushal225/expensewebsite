""" 
options=webdriver.ChromeOptions()
options.add_argument('headless')
driver =webdriver.Chrome()
driver.get("https://www.google.com/search?q=free+currency+converter")
elem = Select(driver.find_element(By.CLASS_NAME, "zuzy3c"))
elem.select_by_visible_text('Euro')
time.sleep(1)
elem1 = driver.find_element(By.CLASS_NAME, "a61j6").get_attribute('value')
print(elem1)
driver.close()
"""

from decimal import Decimal
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
from django.shortcuts import render,redirect
import os
import json
from expensewebsite.settings import BASE_DIR
from .models import UserPreferences
from django.contrib import messages
from expenses.models import Expense
from django.contrib.auth.models import User
from groups import models as group_models
from groups import views as group_views
# Create your views here.


def index(request):
    currency_data=[]
    file_path=os.path.join(BASE_DIR,'currencies.json')
    with open(file_path,'r') as json_file:
        data=json.load(json_file)
        for key,value in data.items():
            currency_data.append({'name':key,'value':value})
    exists=UserPreferences.objects.filter(user=request.user).exists()
    user_preferences=None
    if exists:
       user_preferences =UserPreferences.objects.get(user=request.user)





    if request.method=='GET':
        #import pdb
        #pdb.set_trace()
        return render(request,'preferences/index.html',{'currencies':currency_data,'user_preferences':user_preferences})
    else:
        currency=request.POST['currency']
        if exists:
            previous_currency=UserPreferences.objects.get(user=request.user).currency
            print(previous_currency)
            if previous_currency!=currency:
                options=webdriver.ChromeOptions()
                options.add_argument("--headless=new")
                driver =webdriver.Chrome(options=options)
                driver.get("https://www.google.com/search?q=free+currency+converter")
                elem = Select(driver.find_element(By.CLASS_NAME, "zuzy3c"))
                elem.select_by_visible_text(previous_currency)
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
                expenses=Expense.objects.filter(owner=request.user)
                for expense in expenses:
                    amount=(Decimal(expense.amount)*Decimal(value_of_new_currency))/Decimal(100000)
                    expense.amount=round(amount)
                    expense.save()
            user_preferences.currency=currency
            user_preferences.save()
        else:
            UserPreferences.objects.create(user=request.user,currency=currency)
        messages.success(request,'your preference has been updated')
        return render(request,'preferences/index.html',{'currencies':currency_data,'user_preferences':user_preferences})



def delete_user_acount(request,user):
    if(request.user.username!=user):
        messages.warning(request,'you are trying to delete someone elses account')
        return redirect('expenses')
    if request.method=='GET':
        return render(request,'partials/confirm_deletion.html',{'message':'do you really want to delete your account'})
    else:
        groups_member=group_models.Members.objects.filter(member=request.user)
        group_lists=[]
        for group_member in groups_member:
            print(group_member.group)
            if(group_views.is_admin(request.user,group_member.group) and group_models.Admins.objects.filter(group=group_member.group).count()==1):
                group_lists.append(group_member.group)
            else:
                group_views.exit_group(request,group_member.group,request.user.username)
        if len(group_lists)>=1:
            return render(request,'partials/pending_action.html',{ 'groups':group_lists })
        User.objects.get(username=user).delete()
        messages.warning(request,'your account is deleted successfully')
        return redirect('login')
