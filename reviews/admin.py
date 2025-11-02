from django.contrib import admin
from .models import Review, ReviewImage, Comment, Like, ReviewHistory


class ReviewImageInline(admin.TabularInline):
    model = ReviewImage
    extra = 1


class ReviewHistoryInline(admin.TabularInline):
    model = ReviewHistory
    extra = 0
    readonly_fields = ['created_at']
    can_delete = False


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'book', 'user', 'rating', 'status', 'like_count', 
                   'comment_count', 'created_at']
    list_filter = ['status', 'is_active', 'created_at']
    search_fields = ['book__title', 'user__username', 'title', 'body_md']
    raw_id_fields = ['book', 'user']
    readonly_fields = ['body_html', 'like_count', 'comment_count', 
                      'created_at', 'updated_at', 'edited_at']
    inlines = [ReviewImageInline, ReviewHistoryInline]
    date_hierarchy = 'created_at'


@admin.register(ReviewImage)
class ReviewImageAdmin(admin.ModelAdmin):
    list_display = ['review', 'order', 'caption', 'created_at']
    list_filter = ['created_at']
    search_fields = ['review__title', 'caption']
    raw_id_fields = ['review']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'review', 'user', 'parent', 'status', 'like_count', 'created_at']
    list_filter = ['status', 'is_active', 'created_at']
    search_fields = ['review__title', 'user__username', 'body']
    raw_id_fields = ['review', 'user', 'parent']
    readonly_fields = ['like_count', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'content_type', 'object_id', 'created_at']
    list_filter = ['content_type', 'created_at']
    search_fields = ['user__username']
    raw_id_fields = ['user']
    date_hierarchy = 'created_at'


@admin.register(ReviewHistory)
class ReviewHistoryAdmin(admin.ModelAdmin):
    list_display = ['review', 'created_at']
    list_filter = ['created_at']
    search_fields = ['review__title']
    readonly_fields = ['created_at']
