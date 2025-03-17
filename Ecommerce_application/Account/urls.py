from django.urls import path
from Account import views
# from django.contrib.auth import views as auth_views
from Account.views import * 

urlpatterns = [
    path('reset-password/', views.PasswordResetRequestView.as_view(), name='password_reset'),
    path('reset-password-confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('register_user/', views.SignUp, name='savedata' ),
    path('login_user/', views.user_loginPage, name='login' ),
    path('logout/', views.logout, name='logout' ),
]  
