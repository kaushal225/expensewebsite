from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Source,Income
from django.contrib import messages
from datetime import datetime
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences import models
from datetime import datetime,timedelta


@login_required(login_url='authentication/login')
def index(request):
    incomes=Income.objects.filter(owner=request.user)
    paginator = Paginator(incomes,5)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    currency=models.UserPreferences.objects.get(user=request.user).currency
    context={
        'incomes':incomes,
        'page_obj':page_obj,
        'currency':currency
    }
    return render(request,'income/index.html',context)


def add_income(request):
    sources=Source.objects.all()
    incomes=Income.objects.filter(owner=request.user)
    context={
        'sources':sources,
        'incomes':incomes
    }
    if request.method == 'POST':
        values=request.POST
        context['values']=values
        amount=request.POST['amount']
        description=request.POST['description']
        source=request.POST['source']
        date=request.POST['income_date']
        #print(date)
        if not amount or not description or not source or not date:
            messages.error(request,'please fill all the fields')
            return render(request,'income/add_income.html',context) 
        income=Income.objects.create(owner=request.user,amount=amount,description=description,source=source,date=date)
        income.save()
        messages.success(request,'your income is successfully added to income list')
        return redirect('incomes')
    return render(request,'income/add_income.html',context)


def edit_income(request,id):
    print(id)
    income = Income.objects.get(pk=id)
    income.date=income.date.strftime("%Y-%m-%d")
    sources=Source.objects.all()
    print(income.date)
    context={
        'income':income,
        'values':income,
        'sources':sources
    }
    if request.method == 'POST':
        values=request.POST
        context['values']=values
        amount=request.POST['amount']
        description=request.POST['description']
        source=request.POST['source']
        date=request.POST['income_date']
        #print(date)
        if not amount or not description or not source or not date:
            messages.error(request,'please fill all the fields')
            return render(request,'incomes/edit-income.html',context) 
        income.amount=amount
        income.source=source
        income.description=description
        income.date=date
        income.save()
        messages.success(request,'your income is successfully updated')
        return redirect('income')
    return render(request,'income/edit-income.html',context)


def search_incomes(request):
    if request.method=='POST':
        search_str=json.loads(request.body).get('searchText')
        print(type(search_str))

        incomes=Income.objects.filter(amount__istartswith=search_str,owner=request.user) | Income.objects.filter(
        date__istartswith=search_str,owner=request.user) | Income.objects.filter(
        description__icontains=search_str,owner=request.user) | Income.objects.filter(
        source__icontains=search_str,owner=request.user)

        return JsonResponse(list(incomes.values()),safe=False)
    
def delete_income(request,id):
    income=Income.objects.get(pk=id)
    income.delete()
    messages.success(request,'successfully removed incomes from your list')
    return redirect('incomes')

def income_category_summary(request):
    print('hello you are delusional but this is working just fine')
    todays_date = datetime.now()
    six_months_ago = todays_date-timedelta(days=180)
    incomes=Income.objects.filter(owner=request.user,date__gte=six_months_ago,date__lte=todays_date)
    finalrep={}
    print(incomes)
    def get_source(income_obj):
        return income_obj.source
    source_list=list(set(map(get_source,incomes)))

    for source in source_list:
        finalrep[source]=0
    for income in incomes:
        finalrep[income.source]+=income.amount
    #for (key,val) in finalrep:
        #print((key,val)
    print('hello')
    return JsonResponse({'income_category_data':finalrep},safe='false')


def stats_view(request):
    return render(request,'income/stats.html')