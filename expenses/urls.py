from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns=[
    path('',views.index,name="expenses"),
    path('add-expenses',views.add_expense,name="add-expenses"),
    path('delete-expenses/<int:id>',views.delete_expense,name="delete-expenses"),
    path('edit-expense/<int:id>',views.edit_expense,name='edit-expense'),
    path('search-expenses',csrf_exempt(views.search_expenses),name='search-expenses'),
    path('expense_category_summary',csrf_exempt(views.expense_category_summary),name='expense_category_summary'),
    path('stats',views.stats_view,name='stats'),
    path('list_messages',views.list_inbox_messages,name='list_messages')

]