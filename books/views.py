from rest_framework import generics, filters, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q, Count, Avg
from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Q, F, FloatField, ExpressionWrapper

from .models import Author, Genre, Publisher, Tag, Book, BookView
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
    
    #Lay địa chỉ IP của client
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    # Ghi lại lượt xem sách
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
    """
    API lấy Top 10 sách thịnh hành trong 7 ngày qua.
    Công thức: Score = (Views * 1) + (Shelf Adds * 3) + (Reviews * 5)
    """
    serializer_class = BookListSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None  # Không phân trang, chỉ lấy Top 10

    def get_queryset(self):
        # 1. Xác định mốc thời gian (7 ngày trước)
        last_week = timezone.now() - timedelta(days=7)

        # 2. Truy vấn và Tính điểm
        queryset = Book.objects.filter(is_active=True).annotate(
            # Đếm lượt xem trong tuần (Weight: 1)
            recent_views=Count(
                'book_views', 
                filter=Q(book_views__created_at__gte=last_week)
            ),
            
            # Đếm lượt thêm vào kệ sách trong tuần (Weight: 3)
            # Lưu ý: 'shelf_items' là related_name trong model ShelfItem
            recent_shelves=Count(
                'shelf_items', 
                filter=Q(shelf_items__added_at__gte=last_week)
            ),
            
            # Đếm lượt review trong tuần (Weight: 5)
            # Chỉ tính review public và active
            recent_reviews=Count(
                'reviews', 
                filter=Q(
                    reviews__created_at__gte=last_week,
                    reviews__status='public',
                    reviews__is_active=True
                )
            )
        ).annotate(
            # 3. Tính tổng điểm (Trending Score)
            # Dùng ExpressionWrapper để đảm bảo kiểu dữ liệu Float
            trending_score=ExpressionWrapper(
                (F('recent_views') * 1.0) + 
                (F('recent_shelves') * 3.0) + 
                (F('recent_reviews') * 5.0),
                output_field=FloatField()
            )
        ).filter(
            # Chỉ lấy sách có điểm > 0 (tránh danh sách rỗng tuếch)
            trending_score__gt=0
        ).order_by('-trending_score', '-created_at')[:10]  # Sắp xếp giảm dần

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