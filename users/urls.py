from django.urls import path
from .views import (
    RegisterView, login_view, logout_view,
    ProfileView, UserDetailView, verify_email
)

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('users/<str:username>/', UserDetailView.as_view(), name='user_detail'),
    path('verify/<str:token>/', verify_email, name='verify_email'),
]
