from django.urls import path
from .views import (
    BookListView, BookDetailView,
    AuthorListView, AuthorDetailView,
    GenreListView, GenreDetailView,
    PublisherListView, PublisherDetailView,
    TagListView, TagDetailView,
)

app_name = 'books'

urlpatterns = [
    # Books
    path('', BookListView.as_view(), name='book_list'),
    path('<str:slug>/', BookDetailView.as_view(), name='book_detail'),
    
    # Authors
    path('authors/', AuthorListView.as_view(), name='author_list'),
    path('authors/<str:slug>/', AuthorDetailView.as_view(), name='author_detail'),
    
    # Genres
    path('genres/', GenreListView.as_view(), name='genre_list'),
    path('genres/<str:slug>/', GenreDetailView.as_view(), name='genre_detail'),
    
    # Publishers
    path('publishers/', PublisherListView.as_view(), name='publisher_list'),
    path('publishers/<str:slug>/', PublisherDetailView.as_view(), name='publisher_detail'),
    
    # Tags
    path('tags/', TagListView.as_view(), name='tag_list'),
    path('tags/<str:slug>/', TagDetailView.as_view(), name='tag_detail'),
]
