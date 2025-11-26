from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class Shelf(models.Model):
    """Shelf Model"""
    SYSTEM_TYPE_CHOICES = [
        ('WTR', _('Want to Read')),
        ('READING', _('Reading')),
        ('READ', _('Read')),
    ]
    
    VISIBILITY_CHOICES = [
        ('public', _('Public')),
        ('private', _('Private')),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='shelves')
    name = models.CharField(_('name'), max_length=100)
    system_type = models.CharField(_('system type'), max_length=20, choices=SYSTEM_TYPE_CHOICES, 
                                    null=True, blank=True)
    description = models.TextField(_('description'), blank=True)
    visibility = models.CharField(_('visibility'), max_length=20, choices=VISIBILITY_CHOICES, 
                                  default='public')
    cover_image = models.ImageField(_('cover image'), upload_to='shelves/covers/', null=True, blank=True)
    book_count = models.PositiveIntegerField(_('book count'), default=0)
    is_active = models.BooleanField(_('active'), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('shelf')
        verbose_name_plural = _('shelves')
        ordering = ['-created_at']
        unique_together = ['user', 'system_type']
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['system_type']),
        ]

    def __str__(self):
        return f"{self.user.username}'s {self.name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class ShelfItem(models.Model):
    """Shelf Item Model"""
    shelf = models.ForeignKey(Shelf, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey('books.Book', on_delete=models.CASCADE, related_name='shelf_items')
    added_at = models.DateTimeField(auto_now_add=True)
    order = models.PositiveIntegerField(_('order'), default=0)

    class Meta:
        verbose_name = _('shelf item')
        verbose_name_plural = _('shelf items')
        unique_together = ['shelf', 'book']
        ordering = ['order', '-added_at']
        indexes = [
            models.Index(fields=['shelf', '-added_at']),
            models.Index(fields=['book', '-added_at']),
        ]

    def __str__(self):
        return f"{self.book.title} in {self.shelf.name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update shelf book count
        self.shelf.book_count = self.shelf.items.count()
        self.shelf.save(update_fields=['book_count'])

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        # Update shelf book count
        self.shelf.book_count = self.shelf.items.count()
        self.shelf.save(update_fields=['book_count'])


class ReadingProgress(models.Model):
    """Reading Progress Model"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                            related_name='reading_progress')
    book = models.ForeignKey('books.Book', on_delete=models.CASCADE, related_name='reading_progress')
    
    page = models.PositiveIntegerField(_('page'), null=True, blank=True)
    percent = models.DecimalField(_('percent'), max_digits=5, decimal_places=2, 
                                 null=True, blank=True)
    
    notes = models.TextField(_('notes'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('reading progress')
        verbose_name_plural = _('reading progress')
        unique_together = ['user', 'book']
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['user', '-updated_at']),
            models.Index(fields=['book', '-updated_at']),
        ]

    def __str__(self):
        return f"{self.user.username}'s progress on {self.book.title}"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.page and self.book.pages and self.page > self.book.pages:
            raise ValidationError('Page cannot exceed total pages of the book.')
        if self.percent and (self.percent < 0 or self.percent > 100):
            raise ValidationError('Percent must be between 0 and 100.')

    def save(self, *args, **kwargs):
        # Calculate percent from page if not provided
        if self.page and self.book.pages and not self.percent:
            self.percent = (self.page / self.book.pages) * 100
        # Calculate page from percent if not provided
        elif self.percent and self.book.pages and not self.page:
            self.page = int((self.percent / 100) * self.book.pages)
        
        self.full_clean()
        super().save(*args, **kwargs)
