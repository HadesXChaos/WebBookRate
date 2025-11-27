from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.contenttypes.models import ContentType
from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .models import Review, ReviewImage, Comment, Like
from books.models import Book
from .serializers import (
    ReviewListSerializer, ReviewDetailSerializer, ReviewImageSerializer,
    CommentSerializer, LikeSerializer, ReviewSerializer # <--- NHỚ IMPORT CÁI NÀY
)
from .permissions import IsOwnerOrReadOnly
from users.throttles import CommentThrottle

class ReviewByBookView(APIView):
    """Get Book details for Review by slug"""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        slug = request.query_params.get('slug')
        
        if not slug:
            return Response({'error': 'Missing param "slug"'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            book = Book.objects.get(slug=slug, is_active=True)
            
            data = {
                'id': book.id,
                'title': book.title,
                'slug': book.slug,
                'cover': book.cover.url if book.cover else None,
                'authors': list(book.authors.values_list('name', flat=True)),
                'year': book.year
            }
            return Response(data, status=status.HTTP_200_OK)
            
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)


class ReviewListView(generics.ListCreateAPIView):
    """
    Review List (GET) and Create (POST).
    Đã đổi tên class cho chuẩn RESTful (thường là ListCreateAPIView)
    nhưng nếu urls.py của bạn đang gọi là ReviewListView thì bạn đổi tên class này lại nhé.
    """
    queryset = Review.objects.filter(status='public', is_active=True).select_related(
        'book', 'user'
    ).prefetch_related('images').order_by('-created_at')
    
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    
    filterset_fields = ['book', 'user', 'status'] 
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReviewSerializer 
        return ReviewListSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Review Detail, Update, Delete"""
    queryset = Review.objects.filter(is_active=True).select_related(
        'book', 'user'
    ).prefetch_related('images')
    
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        # Logic chọn serializer của bạn rất chuẩn -> Giữ nguyên
        if self.request.method in ['PUT', 'PATCH']:
            return ReviewSerializer
        return ReviewDetailSerializer

    # --- SỬA PHẦN CACHE TẠI ĐÂY ---

    def retrieve(self, request, *args, **kwargs):
        # 1. Tạo tên key thủ công
        pk = kwargs.get('pk')
        cache_key = f'review_detail_{pk}'
        
        # 2. Thử lấy từ cache
        data = cache.get(cache_key)
        
        if not data:
            # 3. Nếu chưa có, gọi logic gốc để lấy từ DB
            response = super().retrieve(request, *args, **kwargs)
            # 4. Lưu data vào cache 60s
            cache.set(cache_key, response.data, 60)
            return response
        
        # Trả về data từ cache (không query DB)
        return Response(data)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
        # 5. Xóa đúng cái key đã tạo ở trên
        pk = self.kwargs.get('pk')
        cache.delete(f'review_detail_{pk}')

    def perform_destroy(self, instance):
        # 6. Xóa cache khi bài viết bị xóa
        pk = self.kwargs.get('pk')
        cache.delete(f'review_detail_{pk}')
        instance.delete()


@api_view(['POST', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def review_like_view(request, pk):
    """Like/Unlike Review"""
    try:
        review = Review.objects.get(pk=pk, is_active=True)
    except Review.DoesNotExist:
        return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)
    
    content_type = ContentType.objects.get_for_model(Review)
    like, created = Like.objects.get_or_create(
        user=request.user,
        content_type=content_type,
        object_id=review.id
    )
    
    if request.method == 'DELETE':
        like.delete()
        return Response({'message': 'Unliked'}, status=status.HTTP_200_OK)
    
    if not created:
        return Response({'message': 'Already liked'}, status=status.HTTP_200_OK)
    
    return Response({'message': 'Liked'}, status=status.HTTP_201_CREATED)


class CommentListView(generics.ListCreateAPIView):
    """Comment List and Create"""
    queryset = Comment.objects.filter(status='public', is_active=True, parent__isnull=True).select_related(
        'review', 'user'
    ).order_by('created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    throttle_classes = [CommentThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Comment Detail, Update, Delete"""
    queryset = Comment.objects.filter(is_active=True)
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


@api_view(['POST', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def comment_like_view(request, pk):
    """Like/Unlike Comment"""
    try:
        comment = Comment.objects.get(pk=pk, is_active=True)
    except Comment.DoesNotExist:
        return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
    
    content_type = ContentType.objects.get_for_model(Comment)
    like, created = Like.objects.get_or_create(
        user=request.user,
        content_type=content_type,
        object_id=comment.id
    )
    
    if request.method == 'DELETE':
        like.delete()
        return Response({'message': 'Unliked'}, status=status.HTTP_200_OK)
    
    if not created:
        return Response({'message': 'Already liked'}, status=status.HTTP_200_OK)
    
    return Response({'message': 'Liked'}, status=status.HTTP_201_CREATED)