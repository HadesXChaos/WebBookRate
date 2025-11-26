"""
Frontend views for BookReview.vn
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth import logout

from users.models import User
from books.models import Book
from reviews.models import Review


def home_view(request):
    """Homepage view"""
    return render(request, 'home.html')


def explore_view(request):
    """Explore/discover books page"""
    return render(request, 'explore.html')


def login_view(request):
    """Login page"""
    if request.user.is_authenticated:
        from django.shortcuts import redirect
        return redirect('home')
    return render(request, 'auth/login.html')


def register_view(request):
    """Register page"""
    if request.user.is_authenticated:
        from django.shortcuts import redirect
        return redirect('home')
    return render(request, 'auth/register.html')


def password_reset_view(request):
    """Password reset request page"""
    if request.user.is_authenticated:
        from django.shortcuts import redirect
        return redirect('home')
    return render(request, 'auth/password_reset.html')


def user_profile_view(request, username):
    """User profile page"""
    profile_user = get_object_or_404(User, username=username)
    
    # Get counts
    reviews_count = Review.objects.filter(user=profile_user, status='published').count()
    
    context = {
        'profile_user': profile_user,
        'reviews_count': reviews_count,
    }
    return render(request, 'users/profile.html', context)


@login_required
def user_shelves_view(request):
    """User shelves page"""
    return render(request, 'shelves/my_shelves.html')

@login_required
def settings_view(request):
    """User settings page"""
    return render(request, 'users/settings.html')


def search_view(request):
    """Search page"""
    query = request.GET.get('q', '')
    context = {
        'query': query,
    }
    return render(request, 'search/search.html', context)


def notifications_view(request):
    """Notifications page"""
    if not request.user.is_authenticated:
        from django.shortcuts import redirect
        return redirect('login')
    return render(request, 'social/notifications.html')


def logout_view_frontend(request):
    """Frontend logout view - handles both GET and POST"""
    if request.method == 'POST':
        # Delete auth token if using token auth
        if request.user.is_authenticated:
            try:
                if hasattr(request.user, 'auth_token'):
                    request.user.auth_token.delete()
            except:
                pass
            
            # Logout from session
            logout(request)
            messages.success(request, 'Đăng xuất thành công!')
        return redirect('home')
    else:
        # For GET requests, render a page that auto-submits POST
        return render(request, 'auth/logout.html')


def book_list_view(request):
    return render(request, 'books/book_list.html')