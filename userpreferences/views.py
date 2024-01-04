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
from django.shortcuts import render
import os
import json
from expensewebsite.settings import BASE_DIR
from .models import UserPreferences
from django.contrib import messages
from expenses.models import Expense
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
                options.add_argument("--headless")
                driver =webdriver.Chrome()
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



