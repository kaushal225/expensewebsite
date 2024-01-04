from django.urls import path
from .import views
urlpatterns=[
    path('',views.index,name='preferences'),
    path('delete_user,<str:user>',views.delete_user_acount,name='delete_user')
]