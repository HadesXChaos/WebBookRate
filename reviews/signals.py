from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
from django.contrib.contenttypes.models import ContentType

from .models import Review, Comment, Like
from social.models import Notification, Follow


# =========================
# 1. REVIEW: rating + new_review
# =========================

@receiver(post_save, sender=Review)
def handle_review_save(sender, instance: Review, created, **kwargs):
    """
    - Cập nhật avg_rating, rating_count, review_count cho Book
    - Nếu là review mới (created) và public -> gửi thông báo new_review tới follower
    """
    book = instance.book

    # Chỉ tính các review public & active
    public_reviews = Review.objects.filter(
        book=book,
        status='public',
        is_active=True
    )

    # Tổng số review public
    book.review_count = public_reviews.count()

    # Rating (chỉ tính review có rating)
    rated_reviews = public_reviews.exclude(rating__isnull=True)
    if rated_reviews.exists():
        book.avg_rating = rated_reviews.aggregate(avg=Avg('rating'))['avg'] or 0
        book.rating_count = rated_reviews.count()
    else:
        book.avg_rating = 0
        book.rating_count = 0

    book.save(update_fields=['avg_rating', 'rating_count', 'review_count'])

    # --- THÔNG BÁO NEW_REVIEW ---
    # Chỉ gửi khi:
    #   - là review mới tạo (created=True)
    #   - đang ở trạng thái public
    #   - review còn active
    if created and instance.status == 'public' and instance.is_active:
        try:
            # Những user đang follow người viết review
            user_ct = ContentType.objects.get_for_model(instance.user.__class__)
            follower_ids = Follow.objects.filter(
                content_type=user_ct,
                object_id=instance.user_id
            ).values_list('follower_id', flat=True)

            review_ct = ContentType.objects.get_for_model(Review)
            noti_list = []

            for follower_id in follower_ids:
                # Không tự gửi thông báo cho chính mình
                if follower_id == instance.user_id:
                    continue

                noti_list.append(
                    Notification(
                        user_id=follower_id,
                        notification_type='new_review',
                        content_type=review_ct,
                        object_id=instance.id,
                        payload={
                            'message': f'{instance.user.username} đã viết review mới về "{instance.book.title}".'
                        }
                    )
                )

            if noti_list:
                Notification.objects.bulk_create(noti_list, ignore_conflicts=True)
        except Exception as e:
            # Để server không chết nếu lỗi notification
            print(f'Lỗi tạo thông báo new_review: {e}')


@receiver(post_delete, sender=Review)
def handle_review_delete(sender, instance: Review, **kwargs):
    """Khi xóa review -> tính lại rating & review_count của Book"""
    book = instance.book
    public_reviews = Review.objects.filter(
        book=book,
        status='public',
        is_active=True
    )

    book.review_count = public_reviews.count()
    rated_reviews = public_reviews.exclude(rating__isnull=True)
    if rated_reviews.exists():
        book.avg_rating = rated_reviews.aggregate(avg=Avg('rating'))['avg'] or 0
        book.rating_count = rated_reviews.count()
    else:
        book.avg_rating = 0
        book.rating_count = 0

    book.save(update_fields=['avg_rating', 'rating_count', 'review_count'])


# =========================
# 2. LIKE: review_like / comment_like
# =========================

@receiver(post_save, sender=Like)
def handle_like_create(sender, instance: Like, created, **kwargs):
    """
    - Tăng like_count cho Review/Comment
    - Gửi notification review_like / comment_like
    """
    if not created:
        return

    obj = instance.content_object
    ct = ContentType.objects.get_for_model(obj.__class__)

    # Cập nhật like_count nếu model có field này
    if hasattr(obj, 'like_count'):
        from .models import Like as LikeModel
        obj.like_count = LikeModel.objects.filter(
            content_type=ct,
            object_id=obj.id
        ).count()
        obj.save(update_fields=['like_count'])

    # --- Thông báo ---
    try:
        # Like REVIEW
        if isinstance(obj, Review) and obj.user_id != instance.user_id:
            Notification.objects.create(
                user=obj.user,
                notification_type='review_like',
                content_type=ct,
                object_id=obj.id,
                payload={
                    'message': f'{instance.user.username} đã thích review của bạn về "{obj.book.title}".'
                }
            )
        # Like COMMENT
        from .models import Comment as CommentModel
        if isinstance(obj, CommentModel) and obj.user_id != instance.user_id:
            Notification.objects.create(
                user=obj.user,
                notification_type='comment_like',
                content_type=ct,
                object_id=obj.id,
                payload={
                    'message': f'{instance.user.username} đã thích bình luận của bạn.'
                }
            )
    except Exception as e:
        print(f'Lỗi tạo thông báo like: {e}')


@receiver(post_delete, sender=Like)
def handle_like_delete(sender, instance: Like, **kwargs):
    """Khi bỏ like -> cập nhật lại like_count"""
    obj = instance.content_object
    ct = ContentType.objects.get_for_model(obj.__class__)
    if hasattr(obj, 'like_count'):
        from .models import Like as LikeModel
        obj.like_count = LikeModel.objects.filter(
            content_type=ct,
            object_id=obj.id
        ).count()
        obj.save(update_fields=['like_count'])


# =========================
# 3. COMMENT: review_comment / comment_reply
# =========================

@receiver(post_save, sender=Comment)
def handle_comment_save(sender, instance: Comment, created, **kwargs):
    """
    - Cập nhật comment_count cho Review
    - Gửi notification:
        + review_comment: comment vào review của mình
        + comment_reply: reply vào comment của mình
    """
    review = instance.review

    # Cập nhật comment_count (chỉ tính comment public & active)
    public_comments = Comment.objects.filter(
        review=review,
        status='public',
        is_active=True
    )
    review.comment_count = public_comments.count()
    review.save(update_fields=['comment_count'])

    # Nếu không phải comment mới (vd: update) thì thôi
    if not created or instance.status != 'public' or not instance.is_active:
        return

    try:
        comment_ct = ContentType.objects.get_for_model(Comment)

        # Reply vào comment
        if instance.parent:
            parent_user = instance.parent.user
            if parent_user_id := parent_user.id != instance.user_id:
                Notification.objects.create(
                    user=parent_user,
                    notification_type='comment_reply',
                    content_type=comment_ct,
                    object_id=instance.id,
                    payload={
                        'message': f'{instance.user.username} đã trả lời bình luận của bạn trong review về "{review.book.title}".'
                    }
                )

        # Comment trực tiếp vào review
        else:
            review_owner = review.user
            if review_owner.id != instance.user_id:
                Notification.objects.create(
                    user=review_owner,
                    notification_type='review_comment',
                    content_type=comment_ct,
                    object_id=instance.id,
                    payload={
                        'message': f'{instance.user.username} đã bình luận vào review của bạn về "{review.book.title}".'
                    }
                )
    except Exception as e:
        print(f'Lỗi tạo thông báo comment: {e}')


@receiver(post_delete, sender=Comment)
def handle_comment_delete(sender, instance: Comment, **kwargs):
    """Khi xóa comment -> cập nhật lại comment_count của review"""
    review = instance.review
    public_comments = Comment.objects.filter(
        review=review,
        status='public',
        is_active=True
    )
    review.comment_count = public_comments.count()
    review.save(update_fields=['comment_count'])
