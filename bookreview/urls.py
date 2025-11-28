"""
URL configuration for bookreview project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from django.shortcuts import get_object_or_404, render, redirect

from .sitemaps import BookSitemap, AuthorSitemap, ReviewSitemap
from .views import (
    home_view, explore_view, login_view, register_view, password_reset_view,
    user_profile_view, user_shelves_view, settings_view, shelf_detail_view,
    search_view, notifications_view, logout_view_frontend,
    book_list_view, genre_directory_view, genre_detail_view, review_editor_view,
    change_password_view, review_list_frontend,
)
from books.models import Book
from reviews.models import Review

# Frontend views for book and review detail pages
def book_detail_frontend(request, slug):
    """Book detail page"""
    book = get_object_or_404(Book, slug=slug, is_active=True)
    context = {
        'book': book,
    }
    return render(request, 'books/book_detail.html', context)

def review_detail_frontend(request, pk):
    """Review detail page"""
    review = get_object_or_404(Review, pk=pk, is_active=True)
    context = {
        'review': review,
    }
    return render(request, 'reviews/review_detail.html', context)

sitemaps = {
    'books': BookSitemap,
    'authors': AuthorSitemap,
    'reviews': ReviewSitemap,
}

urlpatterns = [
    # Frontend pages
    path('', home_view, name='home'),
    path('explore/', explore_view, name='explore'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('password-reset/', password_reset_view, name='password_reset'),
    path('logout/', logout_view_frontend, name='logout'),
    path('search/', search_view, name='search'),
    path('users/<str:username>/', user_profile_view, name='user_profile'),
    path('shelves/', user_shelves_view, name='user_shelves'),
    path('shelves/<int:shelf_id>/', shelf_detail_view, name='shelf_detail'),
    path('settings/', settings_view, name='settings'),
    path('notifications/', notifications_view, name='notifications'),
    path('books/', book_list_view, name='book_list_view'),
    path('books/genres/', genre_directory_view, name='genre_directory'),
    path('books/genres/<str:slug>/', genre_detail_view, name='genre_detail'),
    path('reviews/', review_list_frontend, name='review_list_frontend'),
    path('reviews/write/', review_editor_view, name='review_editor'),
    
    path('password-change/',change_password_view, name='password_change_page'),
    
    # Frontend detail pages
    path('books/<str:slug>/', book_detail_frontend, name='book_detail_frontend'),
    path('reviews/<int:pk>/', review_detail_frontend, name='review_detail_frontend'),
    
    # API endpoints
    path('api/auth/', include('users.urls')),
    path('api/books/', include('books.urls')),
    path('api/reviews/', include('reviews.urls')),
    path('api/shelves/', include('shelves.urls')),
    path('api/social/', include('social.urls')),
    path('api/moderation/', include('moderation.urls')),
    path('api/search/', include('search.urls')),
    
    # Admin and SEO
    path('admin/', admin.site.urls),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    path('healthz', TemplateView.as_view(template_name='healthz.html')),

    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
