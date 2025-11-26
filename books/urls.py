from django.urls import path
from .views import (
    BookListView, BookDetailView,
    AuthorListView, AuthorDetailView,
    GenreListView, GenreDetailView,
    PublisherListView, PublisherDetailView,
    TagListView, TagDetailView, TrendingBookListView,
)

app_name = 'books'

urlpatterns = [
    # Books
    path('', BookListView.as_view(), name='book_list'),

    # Trending Books
    path('trending/', TrendingBookListView.as_view(), name='book_trending'),
    
    # Authors (must come before catch-all slug pattern)
    path('authors/', AuthorListView.as_view(), name='author_list'),
    path('authors/<str:slug>/', AuthorDetailView.as_view(), name='author_detail'),
    
    # Genres (must come before catch-all slug pattern)
    path('genres/', GenreListView.as_view(), name='genre_list'),
    path('genres/<str:slug>/', GenreDetailView.as_view(), name='genre_detail'),
    
    # Publishers (must come before catch-all slug pattern)
    path('publishers/', PublisherListView.as_view(), name='publisher_list'),
    path('publishers/<str:slug>/', PublisherDetailView.as_view(), name='publisher_detail'),
    
    # Tags (must come before catch-all slug pattern)
    path('tags/', TagListView.as_view(), name='tag_list'),
    path('tags/<str:slug>/', TagDetailView.as_view(), name='tag_detail'),
    
    # Books detail (catch-all pattern must come last)
    path('<str:slug>/', BookDetailView.as_view(), name='book_detail'),

    
]
