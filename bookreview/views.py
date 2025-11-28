"""
Frontend views for BookReview.vn
"""
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.contenttypes.models import ContentType
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth import logout
from django.core.paginator import Paginator  # NEW

from users.models import User
from books.models import Book, Genre
from reviews.models import Review
from social.models import Follow


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

    is_following = False
    if request.user.is_authenticated and request.user != profile_user:
        user_content_type = ContentType.objects.get_for_model(User)
        
        is_following = Follow.objects.filter(
            follower=request.user,
            content_type=user_content_type,
            object_id=profile_user.id
        ).exists()
    
    context = {
        'profile_user': profile_user,
        'reviews_count': reviews_count,
        'is_following': is_following,
    }
    return render(request, 'users/profile.html', context)


@login_required
def user_shelves_view(request):
    """User shelves page"""
    return render(request, 'shelves/my_shelves.html')



@login_required
def shelf_detail_view(request, shelf_id):
    """
    Trang chi tiết 1 kệ sách.
    Dữ liệu chi tiết sẽ được load qua API /api/shelves/<id>/ bằng JavaScript.
    """
    return render(request, 'shelves/shelf_detail.html', {'shelf_id': shelf_id})

@login_required
def settings_view(request):
    """User settings page"""
    return render(request, 'users/settings.html')

@login_required
def change_password_view(request):
    """User settings page"""
    return render(request, 'users/password-change.html')

def review_list_frontend(request):
    """Trang danh sách reviews (frontend, không phải API)."""
    sort = request.GET.get('sort', 'newest')

    qs = Review.objects.filter(status='public', is_active=True) \
        .select_related('book', 'user', 'user__profile') \
        .prefetch_related('book__authors')

    # Sắp xếp
    if sort == 'top_rated':
        qs = qs.order_by('-rating', '-created_at')
    elif sort == 'most_liked':
        qs = qs.order_by('-like_count', '-created_at')
    elif sort == 'most_commented':
        qs = qs.order_by('-comment_count', '-created_at')
    else:
        sort = 'newest'
        qs = qs.order_by('-created_at')

    paginator = Paginator(qs, 10)  # 10 review / trang
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'reviews': page_obj.object_list,
        'sort': sort,
    }
    return render(request, 'reviews/review_list.html', context)


@login_required
def review_editor_view(request):
    """Review editor page with markdown preview and autosave support"""
    review_id = request.GET.get('review')
    
    book_slug = request.GET.get('slug') or request.GET.get('book') 

    existing_review = None
    selected_book = None

    if review_id:
        existing_review = get_object_or_404(Review, pk=review_id, user=request.user)
        selected_book = existing_review.book
    elif book_slug:
        selected_book = get_object_or_404(Book, slug=book_slug, is_active=True)

    initial_review = None
    if existing_review:
        initial_review = {
            'id': existing_review.id,
            'title': existing_review.title,
            'body_md': existing_review.body_md,
            'rating': float(existing_review.rating) if existing_review.rating is not None else None,
            'status': existing_review.status,
            'saved_at': existing_review.updated_at.isoformat() if existing_review.updated_at else None,
            'book': {
                'id': existing_review.book.id,
                'title': existing_review.book.title,
                'slug': existing_review.book.slug,
                'cover': existing_review.book.cover.url if existing_review.book.cover else None,
            },
        }

    selected_book_data = None
    if selected_book:
        authors = list(selected_book.authors.values_list('name', flat=True))
        selected_book_data = {
            'id': selected_book.id,
            'title': selected_book.title,
            'slug': selected_book.slug,
            'cover': selected_book.cover.url if selected_book.cover else None,
            'authors': authors,
            'year': selected_book.year,
            'pages': selected_book.pages,
        }

    storage_key = f"review_draft_user_{request.user.id}"
    if existing_review:
        storage_key += f"_review_{existing_review.id}"
    elif selected_book:
        storage_key += f"_book_{selected_book.slug}"

    context = {
        'selected_book': selected_book,
        'selected_book_data': selected_book_data,
        'existing_review': existing_review,
        'initial_review': initial_review,
        'storage_key': storage_key,
    }
    return render(request, 'reviews/review_editor.html', context)


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
    """Public book list page that hydrates data via REST API"""
    return render(request, 'books/book_list.html')


def genre_directory_view(request):
    """Public genre directory page that hydrates data via REST API"""
    return render(request, 'books/genre_list.html')


def genre_detail_view(request, slug):
    """Genre detail landing page (frontend)"""
    genre = get_object_or_404(Genre, slug=slug, is_active=True)
    context = {
        'genre': genre,
    }
    return render(request, 'books/genre_detail.html', context)