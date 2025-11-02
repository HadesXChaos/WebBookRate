from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, RegexValidator


class Author(models.Model):
    """Author Model"""
    name = models.CharField(_('name'), max_length=200, unique=True)
    slug = models.SlugField(_('slug'), max_length=200, unique=True, blank=True)
    bio = models.TextField(_('biography'), blank=True)
    photo = models.ImageField(_('photo'), upload_to='authors/', null=True, blank=True)
    birth_date = models.DateField(_('birth date'), null=True, blank=True)
    death_date = models.DateField(_('death date'), null=True, blank=True)
    nationality = models.CharField(_('nationality'), max_length=100, blank=True)
    website = models.URLField(_('website'), blank=True)
    is_active = models.BooleanField(_('active'), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('author')
        verbose_name_plural = _('authors')
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('author_detail', kwargs={'slug': self.slug})


class Genre(models.Model):
    """Genre Model"""
    name = models.CharField(_('name'), max_length=100, unique=True)
    slug = models.SlugField(_('slug'), max_length=100, unique=True, blank=True)
    description = models.TextField(_('description'), blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, 
                               blank=True, related_name='children')
    is_active = models.BooleanField(_('active'), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('genre')
        verbose_name_plural = _('genres')
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('genre_detail', kwargs={'slug': self.slug})


class Publisher(models.Model):
    """Publisher Model"""
    name = models.CharField(_('name'), max_length=200, unique=True)
    slug = models.SlugField(_('slug'), max_length=200, unique=True, blank=True)
    description = models.TextField(_('description'), blank=True)
    logo = models.ImageField(_('logo'), upload_to='publishers/', null=True, blank=True)
    website = models.URLField(_('website'), blank=True)
    is_active = models.BooleanField(_('active'), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('publisher')
        verbose_name_plural = _('publishers')
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('publisher_detail', kwargs={'slug': self.slug})


class Tag(models.Model):
    """Tag Model"""
    name = models.CharField(_('name'), max_length=50, unique=True)
    slug = models.SlugField(_('slug'), max_length=50, unique=True, blank=True)
    description = models.TextField(_('description'), blank=True)
    is_active = models.BooleanField(_('active'), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('tags')
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('tag_detail', kwargs={'slug': self.slug})


class Book(models.Model):
    """Book Model"""
    title = models.CharField(_('title'), max_length=500)
    slug = models.SlugField(_('slug'), max_length=500, unique=True, blank=True)
    description = models.TextField(_('description'), blank=True)
    cover = models.ImageField(_('cover'), upload_to='books/covers/', null=True, blank=True)
    
    # Metadata
    year = models.IntegerField(_('year'), null=True, blank=True)
    pages = models.PositiveIntegerField(_('pages'), validators=[MinValueValidator(1)], null=True, blank=True)
    language = models.CharField(_('language'), max_length=10, default='vi')
    
    # Relationships
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, 
                                  null=True, blank=True, related_name='books')
    authors = models.ManyToManyField(Author, related_name='books')
    genres = models.ManyToManyField(Genre, related_name='books')
    tags = models.ManyToManyField(Tag, related_name='books', blank=True)
    
    # Aggregated fields (calculated)
    avg_rating = models.DecimalField(_('average rating'), max_digits=3, decimal_places=2, 
                                     default=0.00)
    rating_count = models.PositiveIntegerField(_('rating count'), default=0)
    review_count = models.PositiveIntegerField(_('review count'), default=0)
    
    # Status
    is_active = models.BooleanField(_('active'), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('book')
        verbose_name_plural = _('books')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug', 'is_active']),
            models.Index(fields=['avg_rating', 'rating_count']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'slug': self.slug})


class BookEdition(models.Model):
    """Book Edition Model"""
    EDITION_FORMAT_CHOICES = [
        ('paperback', _('Paperback')),
        ('hardcover', _('Hardcover')),
        ('ebook', _('E-book')),
        ('audiobook', _('Audiobook')),
    ]
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='editions')
    isbn13 = models.CharField(_('ISBN-13'), max_length=13, unique=True, null=True, blank=True,
                             validators=[RegexValidator(regex=r'^\d{13}$', 
                                                       message='ISBN-13 must be 13 digits')])
    format = models.CharField(_('format'), max_length=20, choices=EDITION_FORMAT_CHOICES,
                            default='paperback')
    published_at = models.DateField(_('published date'), null=True, blank=True)
    language = models.CharField(_('language'), max_length=10, default='vi')
    pages = models.PositiveIntegerField(_('pages'), validators=[MinValueValidator(1)], 
                                        null=True, blank=True)
    is_active = models.BooleanField(_('active'), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('book edition')
        verbose_name_plural = _('book editions')
        ordering = ['-published_at']

    def __str__(self):
        return f"{self.book.title} - {self.get_format_display()}"
