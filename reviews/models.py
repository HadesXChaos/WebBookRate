from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
import bleach
import markdown


class Review(models.Model):
    """Review Model"""
    STATUS_CHOICES = [
        ('draft', _('Draft')),
        ('public', _('Public')),
        ('hidden', _('Hidden')),
    ]
    
    book = models.ForeignKey('books.Book', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    
    title = models.CharField(_('title'), max_length=200)
    body_md = models.TextField(_('body markdown'))
    body_html = models.TextField(_('body html'), blank=True)
    
    rating = models.DecimalField(_('rating'), max_digits=2, decimal_places=1,
                                validators=[MinValueValidator(1), MaxValueValidator(5)],
                                null=True, blank=True)
    
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='public')
    is_active = models.BooleanField(_('active'), default=True)
    
    like_count = models.PositiveIntegerField(_('like count'), default=0)
    comment_count = models.PositiveIntegerField(_('comment count'), default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    edited_at = models.DateTimeField(null=True, blank=True)
    
    # Generic relation for likes
    likes = GenericRelation('Like', related_query_name='review')

    class Meta:
        verbose_name = _('review')
        verbose_name_plural = _('reviews')
        ordering = ['-created_at']
        unique_together = ['book', 'user']
        indexes = [
            models.Index(fields=['book', 'status', '-created_at']),
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f"{self.user.username}'s review of {self.book.title}"

    def save(self, *args, **kwargs):
        # Convert markdown to HTML and sanitize
        if self.body_md:
            html = markdown.markdown(self.body_md, extensions=['extra', 'nl2br'])
            allowed_tags = bleach.sanitizer.ALLOWED_TAGS + ['p', 'br', 'strong', 'em', 'ul', 'ol', 'li', 'blockquote']
            self.body_html = bleach.clean(html, tags=allowed_tags, strip=True)
        
        # Track edit
        if self.pk:
            from django.utils import timezone
            self.edited_at = timezone.now()
        
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('review_detail', kwargs={'pk': self.pk})


class ReviewImage(models.Model):
    """Review Image"""
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(_('image'), upload_to='reviews/images/')
    caption = models.CharField(_('caption'), max_length=200, blank=True)
    order = models.PositiveIntegerField(_('order'), default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('review image')
        verbose_name_plural = _('review images')
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"Image {self.order} for {self.review}"


class Comment(models.Model):
    """Comment Model"""
    STATUS_CHOICES = [
        ('public', _('Public')),
        ('hidden', _('Hidden')),
        ('deleted', _('Deleted')),
    ]
    
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, 
                               related_name='replies')
    
    body = models.TextField(_('body'), max_length=2000)
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='public')
    is_active = models.BooleanField(_('active'), default=True)
    
    like_count = models.PositiveIntegerField(_('like count'), default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Generic relation for likes
    likes = GenericRelation('Like', related_query_name='comment')

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['review', '-created_at']),
            models.Index(fields=['parent', '-created_at']),
        ]

    def __str__(self):
        return f"{self.user.username}'s comment on {self.review}"

    def is_reply(self):
        return self.parent is not None


class Like(models.Model):
    """Like Model - Generic Foreign Key"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('like')
        verbose_name_plural = _('likes')
        unique_together = ['user', 'content_type', 'object_id']
        indexes = [
            models.Index(fields=['content_type', 'object_id', '-created_at']),
        ]

    def __str__(self):
        return f"{self.user.username} liked {self.content_object}"


class ReviewHistory(models.Model):
    """Review Edit History"""
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='history')
    title = models.CharField(max_length=200)
    body_md = models.TextField()
    body_html = models.TextField()
    rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('review history')
        verbose_name_plural = _('review histories')
        ordering = ['-created_at']

    def __str__(self):
        return f"History for {self.review} at {self.created_at}"
