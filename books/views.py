from rest_framework import generics, filters, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import Coalesce
from django.db.models import Count, Q, F, FloatField, ExpressionWrapper
from django.core.paginator import Paginator  # NEW

from .models import Author, Genre, Publisher, Tag, Book, BookView
from .serializers import (
    AuthorSerializer, GenreSerializer, PublisherSerializer, TagSerializer,
    BookListSerializer, BookDetailSerializer, 
)


class BookListView(generics.ListAPIView):
    """Book List with Filters"""
    queryset = Book.objects.filter(is_active=True).select_related('publisher').prefetch_related(
        'authors', 'genres', 'tags'
    )
    serializer_class = BookListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['genres', 'tags', 'year', 'language', 'publisher']
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
    
    #Lay địa chỉ IP của client
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        ip = self.get_client_ip(request)
        user = request.user if request.user.is_authenticated else None
        
        BookView.objects.create(
            book=instance,
            ip_address=ip,
            user=user
        )
        return super().retrieve(request, *args, **kwargs)
    
    def get_object(self):
        slug = self.kwargs.get('slug')
        cache_key = f'book_detail:{slug}'
        book = cache.get(cache_key)
        
        if book is None:
            book = super().get_object()
            cache.set(cache_key, book, 60)  # Cache for 60 seconds
        
        return book
    

class TrendingBookListView(generics.ListAPIView):
    """Trending Books - Based on views, shelves, and reviews in the last 7 days"""
    serializer_class = BookListSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None

    def get_queryset(self):
        last_week = timezone.now() - timedelta(days=7)

        queryset = Book.objects.filter(is_active=True).annotate(
            recent_views=Count(
                'book_views',
                filter=Q(book_views__created_at__gte=last_week)
            ),

            recent_shelves=Coalesce(
                Count(
                    'shelf_items__shelf__user',
                    filter=Q(
                        shelf_items__added_at__gte=last_week,
                        shelf_items__shelf__user__isnull=False
                    ),
                    distinct=True
                ),
                0
            ),

            recent_reviews=Count(
                'reviews',
                filter=Q(
                    reviews__created_at__gte=last_week,
                    reviews__status='public',
                    reviews__is_active=True
                )
            )
        ).annotate(
            trending_score=ExpressionWrapper(
                F('recent_views')     * 1.0   +
                F('recent_shelves')   * 6.0   +
                F('recent_reviews')   * 10.0,
                output_field=FloatField()
            )
        ).filter(trending_score__gt=0)\
         .order_by('-trending_score', '-avg_rating', '-created_at')[:10]

        return queryset


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
    """ Genre Detail with Books """
    queryset = Genre.objects.filter(is_active=True)
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, *args, **kwargs):
        genre = self.get_object()
        
        books = genre.books.filter(is_active=True)\
            .select_related('publisher')\
            .prefetch_related('authors', 'genres', 'tags')\
            .order_by('-avg_rating', '-created_at')

        page = self.paginate_queryset(books)
        
        genre_data = GenreSerializer(genre, context={'request': request}).data

        if page is not None:
            books_data = BookListSerializer(page, many=True, context={'request': request}).data
            return self.get_paginated_response({
                'genre': genre_data,
                'books': books_data
            })

        books_data = BookListSerializer(books, many=True, context={'request': request}).data
        return Response({
            'genre': genre_data,
            'books': books_data
        })

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


class ExploreBooks(generics.ListAPIView):
    """Explore Books with advanced filtering and ordering"""
    class Pagination(PageNumberPagination):
        page_size = 12
        page_size_query_param = 'page_size'
        max_page_size = 100

    pagination_class = Pagination
    serializer_class = BookListSerializer

    def get_queryset(self):
        queryset = Book.objects.filter(is_active=True).prefetch_related('authors', 'genres')

        genre_slug = self.request.query_params.get('genre')
        year = self.request.query_params.get('year')
        min_rating = self.request.query_params.get('min_rating')
        ordering = self.request.query_params.get('ordering')

        if genre_slug:
            queryset = queryset.filter(genres__slug=genre_slug)
        
        if year:
            queryset = queryset.filter(year=year) 
        
        if min_rating:
            try:
                queryset = queryset.filter(avg_rating__gte=float(min_rating))
            except ValueError:
                pass

        valid_ordering = {
            '-rating_count': '-rating_count',
            '-avg_rating': '-avg_rating',
            '-created_at': '-created_at',
            'title': 'title'
        }
        
        if ordering in valid_ordering:
            queryset = queryset.order_by(ordering)
        else:
            queryset = queryset.order_by('-created_at')

        return queryset.distinct()
    

class BookYearsAPIView(generics.ListAPIView):
    """API endpoint to get distinct publication years of books"""
    queryset = Book.objects.none()
    pagination_class = None
    serializer_class = None

    filter_backends = []

    def list(self, request, *args, **kwargs):
        years = Book.objects.filter(is_active=True)\
                            .values_list('year', flat=True)\
                            .distinct()\
                            .order_by('-year')
        
        data = [y for y in years if y is not None]
        
        return Response(data)