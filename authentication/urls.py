from django.urls import path
from . import views 
from django.views.decorators.csrf import csrf_exempt
urlpatterns=[
    path('register',views.RegistrationView.as_view(),name='register'),
    path('login',views.LoginView.as_view(),name='login'),
    path('logout',views.logoutView.as_view(),name='logout'),
    path('validate-username',csrf_exempt(views.UserNameValidationView.as_view()),name="validate-username"),
    path('activate/<uidb64>/<token>',views.verificationView.as_view(),name='activate'),
    path('password-reset/<uidb64>/<token>',views.completePasswordReset.as_view(),name='password-reset'),
    path('password-reset-link',views.RequestPasswordResetEmail.as_view(),name='password-reset-link'),
    path('validate-email',csrf_exempt(views.EmailValidationView.as_view()),name="validate-email"),
]