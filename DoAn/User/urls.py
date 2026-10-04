from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('account/', views.account_view, name='account'),
    path('forgot-password/',views.forgot_password_view,name='forgot_password'),
    path('reset-password/<uidb64>/<token>/',views.reset_password_view,name='password_reset_confirm'),
]