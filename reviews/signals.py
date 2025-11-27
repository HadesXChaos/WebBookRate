from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg, Count
from django.contrib.contenttypes.models import ContentType
from .models import Review, Comment, Like
from social.models import Notification

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



@receiver(post_save, sender=Review)
def check_user_upgrade(sender, instance, created, **kwargs):
    """Check and upgrade user role based on public review count"""
    # Bọc try-except để đảm bảo an toàn tuyệt đối cho luồng chính
    try:
        if instance.status != 'public':
            return

        user = instance.user

        # Chỉ check nếu là reader (để tối ưu performance)
        if user.role != 'reader':
            return

        public_review_count = Review.objects.filter(
            user=user, 
            status='public',
            is_active=True
        ).count()

        UPGRADE_THRESHOLD = 20

        if public_review_count >= UPGRADE_THRESHOLD:
            user.role = 'reviewer'
            user.save(update_fields=['role'])
            
            # Tạo thông báo
            try:
                Notification.objects.create(
                    user=user,
                    notification_type='rank_upgrade',
                    content_type=ContentType.objects.get_for_model(user),
                    object_id=user.id,
                    payload={
                        'message': f'Chúc mừng! Bạn đã viết đủ {UPGRADE_THRESHOLD} bài review và được thăng hạng lên Reviewer.',
                        'new_role': 'Reviewer'
                    }
                )
            except Exception as noti_error:
                print(f"Lỗi tạo notification (không ảnh hưởng review): {noti_error}")

    except Exception as e:
        print(f"Lỗi Critical trong signal thăng hạng: {e}")



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