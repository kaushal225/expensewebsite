from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Custom_groups)
admin.site.register(models.Group_individual_expenses)
admin.site.register(models.Admins)
admin.site.register(models.Members)
