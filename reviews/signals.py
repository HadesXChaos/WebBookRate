from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg, Count
from .models import Review, Comment, Like


@receiver(post_save, sender=Review)
def update_book_rating(sender, instance, created, **kwargs):
    """Update book average rating and review count"""
    book = instance.book
    
    # Recalculate average rating
    ratings = Review.objects.filter(book=book, status='public', is_active=True, rating__isnull=False)
    if ratings.exists():
        book.avg_rating = ratings.aggregate(avg=Avg('rating'))['avg'] or 0
        book.rating_count = ratings.count()
    else:
        book.avg_rating = 0
        book.rating_count = 0
    
    # Update review count
    reviews = Review.objects.filter(book=book, status='public', is_active=True)
    book.review_count = reviews.count()
    
    book.save(update_fields=['avg_rating', 'rating_count', 'review_count'])


@receiver(post_delete, sender=Review)
def update_book_rating_on_delete(sender, instance, **kwargs):
    """Update book rating when review is deleted"""
    update_book_rating(sender, instance, created=False)


@receiver(post_save, sender=Like)
def update_like_count(sender, instance, created, **kwargs):
    """Update like count for review or comment"""
    if created:
        obj = instance.content_object
        if hasattr(obj, 'like_count'):
            obj.like_count += 1
            obj.save(update_fields=['like_count'])


@receiver(post_delete, sender=Like)
def decrease_like_count(sender, instance, **kwargs):
    """Decrease like count when like is deleted"""
    obj = instance.content_object
    if hasattr(obj, 'like_count'):
        obj.like_count = max(0, obj.like_count - 1)
        obj.save(update_fields=['like_count'])


@receiver(post_save, sender=Comment)
def update_review_comment_count(sender, instance, created, **kwargs):
    """Update comment count for review"""
    if created and instance.status == 'public':
        review = instance.review
        review.comment_count = Comment.objects.filter(
            review=review, status='public', is_active=True
        ).count()
        review.save(update_fields=['comment_count'])


@receiver(post_delete, sender=Comment)
def decrease_comment_count(sender, instance, **kwargs):
    """Decrease comment count when comment is deleted"""
    review = instance.review
    review.comment_count = Comment.objects.filter(
        review=review, status='public', is_active=True
    ).count()
    review.save(update_fields=['comment_count'])
