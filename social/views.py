from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.contrib.auth import get_user_model

from .models import Follow, Notification, Collection, CollectionItem
from .serializers import FollowSerializer, NotificationSerializer, CollectionSerializer, CollectionItemSerializer
from books.models import Book, Author

User = get_user_model()


class NotificationListView(generics.ListAPIView):
    """Notification List"""
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_notification_read(request, pk):
    """Mark notification as read"""
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.mark_as_read()
    return Response({'message': 'Notification marked as read'})


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_all_notifications_read(request):
    """Mark all notifications as read"""
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return Response({'message': 'All notifications marked as read'})


class CollectionListView(generics.ListCreateAPIView):
    """Collection List and Create"""
    serializer_class = CollectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            # Show own collections and public collections
            return Collection.objects.filter(
                Q(user=self.request.user) | Q(visibility='public', is_active=True)
            ).prefetch_related('items__book').order_by('-created_at')
        return Collection.objects.filter(
            visibility='public', is_active=True
        ).prefetch_related('items__book').order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CollectionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Collection Detail, Update, Delete"""
    serializer_class = CollectionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Collection.objects.filter(
                Q(user=self.request.user) | Q(visibility='public', is_active=True)
            ).prefetch_related('items__book')
        return Collection.objects.filter(visibility='public', is_active=True).prefetch_related('items__book')

    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You don't have permission to edit this collection.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You don't have permission to delete this collection.")
        instance.delete()


@api_view(['POST', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def collection_item_view(request, collection_id, book_id):
    """Add/Remove book from collection"""
    collection = get_object_or_404(Collection, id=collection_id, user=request.user)
    book = get_object_or_404(Book, id=book_id, is_active=True)
    
    if request.method == 'POST':
        item, created = CollectionItem.objects.get_or_create(
            collection=collection,
            book=book,
            defaults={'order': collection.items.count()}
        )
        if not created:
            return Response({'message': 'Book already in collection'}, status=status.HTTP_200_OK)
        return Response({'message': 'Book added to collection'}, status=status.HTTP_201_CREATED)
    
    # DELETE
    item = get_object_or_404(CollectionItem, collection=collection, book=book)
    item.delete()
    return Response({'message': 'Book removed from collection'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def feed_view(request):
    """User Feed - Reviews from followed users/authors/books"""
    from reviews.models import Review
    from django.db.models import Q
    
    # Get ContentTypes for user, author, and book models
    user_content_type = ContentType.objects.get(model='user')
    author_content_type = ContentType.objects.get(model='author')
    book_content_type = ContentType.objects.get(model='book')
    
    # Get followed users, authors, books
    followed_users = Follow.objects.filter(
        follower=request.user, content_type=user_content_type
    ).values_list('object_id', flat=True)
    
    followed_authors = Follow.objects.filter(
        follower=request.user, content_type=author_content_type
    ).values_list('object_id', flat=True)
    
    followed_books = Follow.objects.filter(
        follower=request.user, content_type=book_content_type
    ).values_list('object_id', flat=True)
    
    # Get reviews from followed users or books
    reviews = Review.objects.filter(
        Q(user_id__in=followed_users) | Q(book_id__in=followed_books) |
        Q(book__authors__id__in=followed_authors),
        status='public',
        is_active=True
    ).select_related('book', 'user').prefetch_related('images').order_by('-created_at')[:20]
    
    from reviews.serializers import ReviewListSerializer
    serializer = ReviewListSerializer(reviews, many=True, context={'request': request})
    return Response(serializer.data)


class FollowToggleView(APIView):
    """Follow or Unfollow User/Author/Book"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = FollowSerializer(data=request.data)
        if serializer.is_valid():
            target_type = serializer.validated_data.get('target_type')
            object_id = serializer.validated_data.get('object_id')
            try:
                content_type = ContentType.objects.get(model=target_type)
            except ContentType.DoesNotExist:
                return Response({'error': 'Invalid target type'}, status=status.HTTP_400_BAD_REQUEST)

            Follow.objects.get_or_create(
                follower=request.user,
                content_type=content_type,
                object_id=object_id
            )
            return Response({'message': 'Followed successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """Unfollow User/Author/Book"""
        target_type = request.data.get('target_type')
        target_id = request.data.get('target_id')

        if not target_type or not target_id:
            return Response({'error': 'Missing target_type or target_id'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            content_type = ContentType.objects.get(model=target_type)
            
            follow = Follow.objects.get(
                follower=request.user,
                content_type=content_type,
                object_id=target_id
            )
            follow.delete()
            
            return Response({'message': 'Unfollowed successfully'}, status=status.HTTP_200_OK)
            
        except ContentType.DoesNotExist:
            return Response({'error': 'Invalid target type'}, status=status.HTTP_400_BAD_REQUEST)
        except Follow.DoesNotExist:
            return Response({'error': 'Not following'}, status=status.HTTP_404_NOT_FOUND)