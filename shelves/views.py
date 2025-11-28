from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.db.models import Exists, OuterRef
from rest_framework.permissions import IsAuthenticated

from .models import Shelf, ShelfItem, ReadingProgress
from .serializers import ShelfSerializer, ShelfItemSerializer, ReadingProgressSerializer
from books.models import Book

User = get_user_model()


class ShelfListView(generics.ListCreateAPIView):
    """Shelf List and Create"""
    serializer_class = ShelfSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = Shelf.objects.filter(
                user=self.request.user
            ).prefetch_related('items__book').order_by('-created_at')

            check_book_id = self.request.query_params.get('check_book_id')
            
            if check_book_id:
                is_in_shelf = ShelfItem.objects.filter(
                    shelf=OuterRef('pk'),
                    book_id=check_book_id
                )
                queryset = queryset.annotate(has_book=Exists(is_in_shelf))
            # ---------------------------------------

            return queryset

        return Shelf.objects.filter(
            visibility='public', is_active=True
        ).prefetch_related('items__book').order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ShelfDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Shelf Detail, Update, Delete"""
    serializer_class = ShelfSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if self.request.method in ['GET']:
            return Shelf.objects.filter(
                Q(user=user) | Q(visibility='public', is_active=True)
            ).prefetch_related('items__book')
        return Shelf.objects.filter(user=user).prefetch_related('items__book')


@api_view(['POST', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def shelf_item_view(request, shelf_id, book_id):
    """Add/Remove book from shelf"""
    shelf = get_object_or_404(Shelf, id=shelf_id, user=request.user)
    book = get_object_or_404(Book, id=book_id, is_active=True)
    
    if request.method == 'POST':
        item, created = ShelfItem.objects.get_or_create(
            shelf=shelf,
            book=book,
            defaults={'order': shelf.items.count()}
        )
        if not created:
            return Response({'message': 'Book already in shelf'}, status=status.HTTP_200_OK)
        return Response({'message': 'Book added to shelf'}, status=status.HTTP_201_CREATED)
    
    # DELETE
    item = get_object_or_404(ShelfItem, shelf=shelf, book=book)
    item.delete()
    return Response({'message': 'Book removed from shelf'}, status=status.HTTP_200_OK)


class ReadingProgressListView(generics.ListCreateAPIView):
    """Reading Progress List and Create"""
    serializer_class = ReadingProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ReadingProgress.objects.filter(user=self.request.user).select_related('book').order_by('-updated_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReadingProgressDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Reading Progress Detail, Update, Delete"""
    serializer_class = ReadingProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ReadingProgress.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class UserShelvesView(generics.ListAPIView):
    """Get user's shelves"""
    serializer_class = ShelfSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        return Shelf.objects.filter(user_id=user_id).order_by("-id")
