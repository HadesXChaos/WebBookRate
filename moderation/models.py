from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Report(models.Model):
    """Report Model - Generic Foreign Key for reporting content"""
    REASON_CHOICES = [
        ('spam', _('Spam')),
        ('inappropriate', _('Inappropriate Content')),
        ('harassment', _('Harassment')),
        ('copyright', _('Copyright Violation')),
        ('misinformation', _('Misinformation')),
        ('other', _('Other')),
    ]
    
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('in_review', _('In Review')),
        ('resolved', _('Resolved')),
        ('rejected', _('Rejected')),
    ]
    
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                                related_name='reports')
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    reason = models.CharField(_('reason'), max_length=50, choices=REASON_CHOICES)
    note = models.TextField(_('note'), blank=True)
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='pending')
    
    moderator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
                                  null=True, blank=True, related_name='moderated_reports')
    moderator_note = models.TextField(_('moderator note'), blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _('report')
        verbose_name_plural = _('reports')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['reporter', '-created_at']),
            models.Index(fields=['content_type', 'object_id']),
        ]

    def __str__(self):
        return f"Report {self.id} - {self.get_reason_display()}"


class ModeratorAction(models.Model):
    """Moderator Action Log"""
    ACTION_CHOICES = [
        ('hide', _('Hide Content')),
        ('delete', _('Delete Content')),
        ('warn', _('Warn User')),
        ('suspend', _('Suspend User')),
        ('ban', _('Ban User')),
        ('approve', _('Approve Content')),
        ('reject', _('Reject Report')),
    ]
    
    moderator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                                 related_name='moderator_actions')
    
    action = models.CharField(_('action'), max_length=50, choices=ACTION_CHOICES)
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    report = models.ForeignKey(Report, on_delete=models.SET_NULL, null=True, blank=True, 
                               related_name='actions')
    
    note = models.TextField(_('note'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('moderator action')
        verbose_name_plural = _('moderator actions')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['moderator', '-created_at']),
            models.Index(fields=['action', '-created_at']),
            models.Index(fields=['content_type', 'object_id']),
        ]

    def __str__(self):
        return f"{self.moderator.username} - {self.get_action_display()}"
