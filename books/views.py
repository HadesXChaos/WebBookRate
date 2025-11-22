from rest_framework import generics, filters, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q, Count, Avg
from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers

from .models import Author, Genre, Publisher, Tag, Book
from .serializers import (
    AuthorSerializer, GenreSerializer, PublisherSerializer, TagSerializer,
    BookListSerializer, BookDetailSerializer
)


class BookListView(generics.ListAPIView):
    """Book List with Filters"""
    queryset = Book.objects.filter(is_active=True).select_related('publisher').prefetch_related(
        'authors', 'genres', 'tags'
    )
    serializer_class = BookListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['genres', 'tags', 'year', 'language']
    search_fields = ['title', 'description', 'authors__name', 'tags__name']
    ordering_fields = ['created_at', 'avg_rating', 'rating_count', 'review_count', 'title']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by rating range
        min_rating = self.request.query_params.get('min_rating')
        if min_rating:
            queryset = queryset.filter(avg_rating__gte=min_rating)
        
        # Filter by review count
        min_reviews = self.request.query_params.get('min_reviews')
        if min_reviews:
            queryset = queryset.filter(review_count__gte=min_reviews)
        
        return queryset


class BookDetailView(generics.RetrieveAPIView):
    """Book Detail - Cached for 60 seconds"""
    queryset = Book.objects.filter(is_active=True).select_related('publisher').prefetch_related(
        'authors', 'genres', 'tags', 'editions'
    )
    serializer_class = BookDetailSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]
    
    @method_decorator(cache_page(60))  # Cache for 60 seconds
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def get_object(self):
        slug = self.kwargs.get('slug')
        cache_key = f'book_detail:{slug}'
        book = cache.get(cache_key)
        
        if book is None:
            book = super().get_object()
            cache.set(cache_key, book, 60)  # Cache for 60 seconds
        
        return book


class AuthorListView(generics.ListAPIView):
    """Author List - Cached for 5 minutes"""
    queryset = Author.objects.filter(is_active=True)
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'bio']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    @method_decorator(cache_page(300))  # Cache for 5 minutes
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class AuthorDetailView(generics.RetrieveAPIView):
    """Author Detail"""
    queryset = Author.objects.filter(is_active=True).prefetch_related('books')
    serializer_class = AuthorSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]


class GenreListView(generics.ListAPIView):
    """Genre List - Cached for 5 minutes"""
    queryset = Genre.objects.filter(is_active=True)
    serializer_class = GenreSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name']
    ordering = ['name']
    
    @method_decorator(cache_page(300))  # Cache for 5 minutes
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class GenreDetailView(generics.RetrieveAPIView):
    """Genre Detail"""
    queryset = Genre.objects.filter(is_active=True)
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]


class PublisherListView(generics.ListAPIView):
    """Publisher List - Cached for 5 minutes"""
    queryset = Publisher.objects.filter(is_active=True)
    serializer_class = PublisherSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    @method_decorator(cache_page(300))  # Cache for 5 minutes
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class PublisherDetailView(generics.RetrieveAPIView):
    """Publisher Detail"""
    queryset = Publisher.objects.filter(is_active=True).prefetch_related('books')
    serializer_class = PublisherSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]


class TagListView(generics.ListAPIView):
    """Tag List - Cached for 5 minutes"""
    queryset = Tag.objects.filter(is_active=True)
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name']
    ordering = ['name']
    
    @method_decorator(cache_page(300))  # Cache for 5 minutes
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class TagDetailView(generics.RetrieveAPIView):
    """Tag Detail"""
    queryset = Tag.objects.filter(is_active=True)
    serializer_class = TagSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]
