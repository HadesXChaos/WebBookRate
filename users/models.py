from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class User(AbstractUser):
    """Custom User Model"""
    email = models.EmailField(_('email address'), unique=True)
    is_verified = models.BooleanField(_('verified'), default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-created_at']

    def __str__(self):
        return self.username


class Profile(models.Model):
    """User Profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=1000, blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    language = models.CharField(max_length=10, default='vi', choices=[
        ('vi', 'Tiếng Việt'),
        ('en', 'English'),
    ])
    timezone = models.CharField(max_length=50, default='Asia/Ho_Chi_Minh')
    
    # Notification settings
    notify_follow = models.BooleanField(default=True)
    notify_review_like = models.BooleanField(default=True)
    notify_comment = models.BooleanField(default=True)
    notify_mention = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def get_absolute_url(self):
        return reverse('user_profile', kwargs={'username': self.user.username})


class EmailVerification(models.Model):
    """Email Verification Token"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_verifications')
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('email verification')
        verbose_name_plural = _('email verifications')
        ordering = ['-created_at']

    def __str__(self):
        return f"Verification for {self.user.email}"


class PasswordResetToken(models.Model):
    """Password Reset Token"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_tokens')
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('password reset token')
        verbose_name_plural = _('password reset tokens')
        ordering = ['-created_at']

    def __str__(self):
        return f"Password reset for {self.user.email}"