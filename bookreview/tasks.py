from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.db.models import Avg, Count, Sum, Q
from django.core.cache import cache
from books.models import Book
from reviews.models import Review


@shared_task
def update_book_ratings():
    """Update book ratings - Run periodically"""
    books = Book.objects.filter(is_active=True)
    for book in books:
        ratings = Review.objects.filter(
            book=book,
            status='public',
            is_active=True,
            rating__isnull=False
        )
        if ratings.exists():
            book.avg_rating = ratings.aggregate(avg=Avg('rating'))['avg'] or 0
            book.rating_count = ratings.count()
        else:
            book.avg_rating = 0
            book.rating_count = 0
        
        book.review_count = Review.objects.filter(
            book=book,
            status='public',
            is_active=True
        ).count()
        
        book.save(update_fields=['avg_rating', 'rating_count', 'review_count'])


@shared_task
def calculate_trending_books():
    """Calculate trending books based on recent reviews and ratings"""
    # Get books with reviews in the last 7 days
    week_ago = timezone.now() - timedelta(days=7)
    
    trending_books = Book.objects.filter(
        reviews__created_at__gte=week_ago,
        is_active=True
    ).annotate(
        recent_reviews=Count('reviews', filter=Q(reviews__created_at__gte=week_ago)),
        avg_rating=Avg('reviews__rating', filter=Q(
            reviews__status='public',
            reviews__is_active=True,
            reviews__rating__isnull=False
        ))
    ).order_by('-recent_reviews', '-avg_rating')[:20]
    
    # Cache the results
    cache.set('trending_books', list(trending_books.values_list('id', flat=True)), 3600 * 6)
    
    return f"Calculated trending books: {trending_books.count()}"


@shared_task
def cleanup_old_notifications():
    """Clean up old read notifications"""
    from social.models import Notification
    from datetime import timedelta
    
    # Delete read notifications older than 30 days
    cutoff_date = timezone.now() - timedelta(days=30)
    deleted = Notification.objects.filter(
        is_read=True,
        created_at__lt=cutoff_date
    ).delete()
    
    return f"Deleted {deleted[0]} old notifications"
