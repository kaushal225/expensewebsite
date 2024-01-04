from django.forms import ModelForm
from . import models
from django import forms

class Create_group(ModelForm):


    class Meta:
        model=models.Custom_groups
        fields=['group_name','group_password']
        widgets={
            'group_password':forms.PasswordInput()
        }