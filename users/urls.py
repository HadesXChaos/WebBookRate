from django.urls import path,include
from .views import (
    RegisterView, login_view, logout_view,
    ProfileView, UserDetailView, verify_email,
    password_reset_request, password_reset_confirm,password_change,
)

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('users/<str:username>/', UserDetailView.as_view(), name='user_detail'),
    path('verify/<str:token>/', verify_email, name='verify_email'),
    path('password-reset/', password_reset_request, name='password_reset_request'),
    path('password-reset/<str:token>/', password_reset_confirm, name='password_reset_confirm'),
    path('password-change/',password_change,name='password_change'),
]
