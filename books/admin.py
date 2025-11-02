from django.contrib import admin
from .models import Author, Genre, Publisher, Tag, Book, BookEdition


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'nationality', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'bio']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent', 'is_active', 'created_at']
    list_filter = ['is_active', 'parent', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'website', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']


class BookEditionInline(admin.TabularInline):
    model = BookEdition
    extra = 1


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'year', 'avg_rating', 'rating_count', 
                   'review_count', 'is_active', 'created_at']
    list_filter = ['is_active', 'year', 'genres', 'created_at']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['authors', 'genres', 'tags']
    readonly_fields = ['avg_rating', 'rating_count', 'review_count', 
                      'created_at', 'updated_at']
    inlines = [BookEditionInline]


@admin.register(BookEdition)
class BookEditionAdmin(admin.ModelAdmin):
    list_display = ['book', 'isbn13', 'format', 'published_at', 'language', 'is_active']
    list_filter = ['format', 'language', 'is_active', 'published_at']
    search_fields = ['book__title', 'isbn13']
    readonly_fields = ['created_at', 'updated_at']
