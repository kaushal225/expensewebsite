from django.db import models
from django.contrib.auth.models import User
from groups import models as group_models
# Create your models here.

class UserPreferences(models.Model):
    user = models.OneToOneField(to=User,on_delete=models.CASCADE)
    currency = models.CharField(max_length=55,blank=True,null=True,default='United States Dollar')

    def __str__(self) -> str:
        return str(self.user)+'s'+' preference'
    

