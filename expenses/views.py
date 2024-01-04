from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Category,Expense
from django.contrib import messages
from datetime import datetime,timedelta
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences import models
from groups import models as group_models

def get_messages(user):
    inbox_messages=list(group_models.Inbox.objects.filter(user=user,sent=False).values())
    
    print(inbox_messages)
    return inbox_messages


def list_inbox_messages(request):
    inbox_messages=get_messages(request.user)
    print(inbox_messages)
    context={'messages':inbox_messages}
    #context['messages']=inbox_messages
    print(context['messages'])
    return render(request,'expenses/list_inbox.html',context)     



def search_expenses(request):
    if request.method=='POST':
        search_str=json.loads(request.body).get('searchText')
        print(type(search_str))

        expenses=Expense.objects.filter(amount__istartswith=search_str,owner=request.user) | Expense.objects.filter(
        date__istartswith=search_str,owner=request.user) | Expense.objects.filter(
        description__icontains=search_str,owner=request.user) | Expense.objects.filter(
        category__icontains=search_str,owner=request.user)

        return JsonResponse(list(expenses.values()),safe=False)


@login_required(login_url='authentication/login')
def index(request):
    recieved_messages=get_messages(request.user)
    print(recieved_messages)
    expenses=Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses,5)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    currency='no currency set'
    try:
        currency=models.UserPreferences.objects.get(user=request.user).currency
    except Exception:
        print('user currently have no currency')
    context={
        'expenses':expenses,
        'page_obj':page_obj,
        'currency':currency
    }
    #print(request.current_app)
    return render(request,'expenses/index.html',context)


def add_expense(request):
    categories=Category.objects.all()
    expenses=Expense.objects.filter(owner=request.user)
    context={
        'categories':categories,
        'expenses':expenses
    }
    if request.method == 'POST':
        values=request.POST
        context['values']=values
        amount=request.POST['amount']
        description=request.POST['description']
        category=request.POST['category']
        date=request.POST['expense_date']
        #print(date)
        if not amount or not description or not category or not date:
            messages.error(request,'please fill all the fields')
            return render(request,'expenses/add_expense.html',context) 
        expense=Expense.objects.create(owner=request.user,amount=amount,description=description,category=category,date=date)
        expense.save()
        messages.success(request,'your expense is successfully added to expense list')
        return redirect('expenses')
    print(categories)
    return render(request,'expenses/add_expense.html',context)



def edit_expense(request,id):
    expense = Expense.objects.get(pk=id)
    if(expense.owner!=request.user):
        messages.warning(request,'not your expenses')
        return redirect('expenses')
    expense.date=expense.date.strftime("%Y-%m-%d")
    categories=Category.objects.all()
    print(expense.date)
    context={
        'expense':expense,
        'values':expense,
        'categories':categories
    }
    if request.method == 'POST':
        values=request.POST
        context['values']=values
        amount=request.POST['amount']
        description=request.POST['description']
        category=request.POST['category']
        date=request.POST['expense_date']
        #print(date)
        if not amount or not description or not category or not date:
            messages.error(request,'please fill all the fields')
            return render(request,'expenses/edit-expense.html',context) 
        expense.amount=amount
        expense.category=category
        expense.description=description
        expense.date=date
        expense.save()
        messages.success(request,'your expense is successfully updated')
        return redirect('expenses')
    return render(request,'expenses/edit-expense.html',context)


def delete_expense(request,id):
    expense=Expense.objects.get(pk=id)
    if(expense.owner!=request.user):
        messages.warning(request,'not your expenses')
        return redirect('expenses')
    if request.method=='GET':

        return render(request,'partials/confirm_deletion.html',{'message':'do you really want to delete this expense'})
    else:
        expense=Expense.objects.get(pk=id)
        expense.delete()
        messages.success(request,'successfully removed expenses from your list')
        return redirect('expenses')


def expense_category_summary(request):
    if request.method=='POST':
        todays_date = datetime.now()
        six_months_ago = todays_date-timedelta(days=180)
        expenses=Expense.objects.filter(owner=request.user,date__gte=six_months_ago,date__lte=todays_date)
        finalrep={}
        print(expenses)
        def get_category(expense):
            return expense.category
        category_list=list(set(map(get_category,expenses)))
        for c in category_list:
            print(c)
        for category in category_list:
            finalrep[category]=0
        for expense in expenses:
            finalrep[expense.category]+=expense.amount
        return JsonResponse({'expense_category_data':finalrep},safe=False)
    return render(request,'expenses/stats.html')


def stats_view(request):
    return render(request,'expenses/stats.html')