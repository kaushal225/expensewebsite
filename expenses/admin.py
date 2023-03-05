from django.contrib import admin
from . import models 
# Register your models here.

class ExpenseAdmin(admin.ModelAdmin):
    list_display=('amount','date','owner','category')
    search_fields=('category','date')

admin.site.register(models.Category)
admin.site.register(models.Expense,ExpenseAdmin)
