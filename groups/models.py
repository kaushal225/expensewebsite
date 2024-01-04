from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.contrib.auth.hashers import make_password
from django.forms import widgets
from django import forms
# Create your models here.

class DateInput(forms.DateInput):
    input_type = 'date'

class Custom_groups(models.Model):
    group_name=models.CharField(primary_key=True,max_length=255)
    #group_admin=models.ForeignKey(to=User,on_delete=models.CASCADE)
    group_password=models.CharField(max_length=255,null=False)
    def __str__(self):
        return self.group_name
    def save(self,**kwargs):
        self.group_password=make_password(self.group_password)
        super().save(**kwargs)

class Members(models.Model):
    group=models.ForeignKey(to=Custom_groups,on_delete=models.CASCADE)
    member=models.ForeignKey(to=User,on_delete=models.CASCADE)


    class Meta:
        constraints=[
        models.UniqueConstraint(fields=['group','member'],name='group_member_constraint')
        ]
    def __str__(self):
        return self.group.group_name

class Group_summary(models.Model):
    group_name=models.ForeignKey(to=Custom_groups,on_delete=models.CASCADE)
    member_name=models.ForeignKey(to=User ,on_delete=models.CASCADE)
    member_total_contribution=models.DecimalField(max_digits=20,decimal_places=5,null=False)
    
    def __str__(self):
        return ""


class Group_individual_expenses(models.Model):
    individual_name=models.ForeignKey(to=User,on_delete=models.CASCADE)
    expense_date=models.DateField(default=now)
    expense_amount=models.DecimalField(max_digits=20,decimal_places=5)
    description=models.CharField(max_length=255)
    group=models.ForeignKey(to=Custom_groups,on_delete=models.CASCADE)

class Inbox(models.Model):
    user=models.ForeignKey(to=User,on_delete=models.CASCADE)
    group=models.ForeignKey(to=Custom_groups,on_delete=models.CASCADE)
    sent=models.BooleanField(default=False)

    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['user','group'],name='unique_inbox_constraint')
            ]

    def __str__(self):
        return self.user+self.group

class PermissionToVisit(models.Model):
    user=models.ForeignKey(to=User,on_delete=models.CASCADE)
    permission_for_group=models.ForeignKey(to=Custom_groups,on_delete=models.CASCADE)

    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['user','permission_for_group'],name='unique_permission_to_visit')
            ]


class Admins(models.Model):
    user=models.ForeignKey(to=User,on_delete=models.CASCADE)
    group=models.ForeignKey(to=Custom_groups,on_delete=models.CASCADE)
    
    class Meta:
       constraints=[ 
           models.UniqueConstraint(fields=['user','group'],name='unique_Admins_constraint')    
       ]

class Group_currency(models.Model):
    group=models.ForeignKey(to=Custom_groups,on_delete=models.CASCADE)
    currency=models.CharField(max_length=255,default='United States Dollar')

    def __str__(self) -> str:
        return str(self.group)+' preferences'

class Group_notification(models.Model):
    user_notification_for=models.ForeignKey(to=User,on_delete=models.CASCADE)
    user_involved=models.CharField(max_length=255,null=True)
    date=models.DateField(default=now)
    admin_involved=models.CharField(max_length=255,null=True)
    group=models.CharField(max_length=255,null=False)
    admin_status_change=models.BooleanField(default=False)
    request_accepted=models.BooleanField(default=False)
    request_denied=models.BooleanField(default=False)