from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns=[
    path('',views.index,name="incomes"),
    path('add-incomes',views.add_income,name="add-income"),
    path('delete-incomes/<int:id>',views.delete_income,name="delete-income"),
    path('edit-income/<int:id>',views.edit_income,name='edit-income'),
    path('search-incomes/',csrf_exempt(views.search_incomes),name='search-incomes'),
    path('income-stats/',views.stats_view,name='income_stats'),
    path('income-category-summary',csrf_exempt(views.income_category_summary),name='income-category-summary'),
]