from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import ValidationError
import json


class Follow(models.Model):
    """Follow Model - Generic Foreign Key for following users/authors/books"""
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                                  related_name='following')
    
    # Generic foreign key to the target object (User/Author/Book)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    target = GenericForeignKey('content_type', 'object_id')
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('follow')
        verbose_name_plural = _('follows')
        unique_together = ['follower', 'content_type', 'object_id'] 
        indexes = [
            models.Index(fields=['follower', '-created_at']),
            models.Index(fields=['content_type', 'object_id', '-created_at']),
        ]

    def __str__(self):
        return f"{self.follower.username} follows {self.target}"

    def clean(self):
        if self.target == self.follower:
            raise ValidationError(_("You cannot follow yourself."))

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Notification(models.Model):
    """Notification Model"""
    TYPE_CHOICES = [
        ('follow', _('New Follower')),
        ('review_like', _('Review Liked')),
        ('review_comment', _('Review Commented')),
        ('review_mention', _('Mentioned in Review')),
        ('comment_reply', _('Comment Replied')),
        ('comment_like', _('Comment Liked')),
        ('new_review', _('New Review from Following')),
        ('collection_item', _('Added to Collection')),
        ('rank_upgrade', _('Rank Upgraded')),
        ('system', _('System Message')),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                            related_name='notifications')
    notification_type = models.CharField(_('type'), max_length=50, choices=TYPE_CHOICES)
    
    # Generic foreign key to the object that triggered the notification
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # JSON payload for additional data
    payload = models.JSONField(_('payload'), default=dict, blank=True)
    
    is_read = models.BooleanField(_('read'), default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('notification')
        verbose_name_plural = _('notifications')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read', '-created_at']),
            models.Index(fields=['notification_type', '-created_at']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.get_notification_type_display()}"

    def mark_as_read(self):
        self.is_read = True
        self.save(update_fields=['is_read'])


class Collection(models.Model):
    """Collection Model"""
    VISIBILITY_CHOICES = [
        ('public', _('Public')),
        ('private', _('Private')),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                            related_name='collections')
    name = models.CharField(_('name'), max_length=200)
    slug = models.SlugField(_('slug'), max_length=200, blank=True)
    description = models.TextField(_('description'), blank=True)
    cover_image = models.ImageField(_('cover image'), upload_to='collections/covers/', 
                                   null=True, blank=True)
    visibility = models.CharField(_('visibility'), max_length=20, choices=VISIBILITY_CHOICES, 
                                 default='public')
    book_count = models.PositiveIntegerField(_('book count'), default=0)
    is_active = models.BooleanField(_('active'), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('collection')
        verbose_name_plural = _('collections')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['visibility', '-created_at']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class CollectionItem(models.Model):
    """Collection Item Model"""
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey('books.Book', on_delete=models.CASCADE, related_name='collection_items')
    notes = models.TextField(_('notes'), blank=True)
    order = models.PositiveIntegerField(_('order'), default=0)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('collection item')
        verbose_name_plural = _('collection items')
        unique_together = ['collection', 'book']
        ordering = ['order', '-added_at']
        indexes = [
            models.Index(fields=['collection', '-added_at']),
            models.Index(fields=['book', '-added_at']),
        ]

    def __str__(self):
        return f"{self.book.title} in {self.collection.name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update collection book count
        self.collection.book_count = self.collection.items.count()
        self.collection.save(update_fields=['book_count'])

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        # Update collection book count
        self.collection.book_count = self.collection.items.count()
        self.collection.save(update_fields=['book_count'])
