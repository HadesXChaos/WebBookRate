from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q
from django.contrib.postgres.search import SearchVector, TrigramSimilarity

from books.models import Book, Author
from reviews.models import Review
from books.serializers import BookListSerializer, AuthorSerializer
from reviews.serializers import ReviewListSerializer


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def search_view(request):
    """Unified Search View"""
    query = request.query_params.get('q', '').strip()
    search_type = request.query_params.get('type', 'all')  # all, books, authors, reviews
    
    if not query:
        return Response({
            'books': [],
            'authors': [],
            'reviews': [],
            'total': 0
        })
    
    results = {
        'books': [],
        'authors': [],
        'reviews': [],
        'total': 0
    }
    
    # Search Books
    if search_type in ['all', 'books']:
        books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(authors__name__icontains=query) |
            Q(tags__name__icontains=query),
            is_active=True
        ).distinct().select_related('publisher').prefetch_related('authors', 'genres')[:20]
        results['books'] = BookListSerializer(books, many=True, context={'request': request}).data
    
    # Search Authors
    if search_type in ['all', 'authors']:
        authors = Author.objects.filter(
            Q(name__icontains=query) |
            Q(bio__icontains=query),
            is_active=True
        ).distinct()[:20]
        results['authors'] = AuthorSerializer(authors, many=True, context={'request': request}).data
    
    # Search Reviews
    if search_type in ['all', 'reviews']:
        reviews = Review.objects.filter(
            Q(title__icontains=query) |
            Q(body_md__icontains=query) |
            Q(book__title__icontains=query),
            status='public',
            is_active=True
        ).distinct().select_related('book', 'user').prefetch_related('images')[:20]
        results['reviews'] = ReviewListSerializer(reviews, many=True, context={'request': request}).data
    
    results['total'] = len(results['books']) + len(results['authors']) + len(results['reviews'])
    
    return Response(results)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def autocomplete_view(request):
    """Autocomplete Search"""
    query = request.query_params.get('q', '').strip()
    search_type = request.query_params.get('type', 'books')  # books, authors
    
    if not query or len(query) < 2:
        return Response({'suggestions': []})
    
    suggestions = []
    
    if search_type == 'books':
        books = Book.objects.filter(
            title__icontains=query,
            is_active=True
        ).values_list('title', flat=True)[:10]
        suggestions = [{'text': title, 'type': 'book'} for title in books]
        
    elif search_type == 'authors':
        authors = Author.objects.filter(
            name__icontains=query,
            is_active=True
        ).values_list('name', flat=True)[:10]
        suggestions = [{'text': name, 'type': 'author'} for name in authors]
    
    return Response({'suggestions': suggestions})
