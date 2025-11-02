from django.contrib import admin
from .models import Follow, Notification, Collection, CollectionItem


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['follower', 'content_type', 'object_id', 'created_at']
    list_filter = ['content_type', 'created_at']
    search_fields = ['follower__username']
    raw_id_fields = ['follower', 'content_type']
    date_hierarchy = 'created_at'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['user__username']
    raw_id_fields = ['user']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'


class CollectionItemInline(admin.TabularInline):
    model = CollectionItem
    extra = 1
    raw_id_fields = ['book']


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'visibility', 'book_count', 'is_active', 'created_at']
    list_filter = ['visibility', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'user__username']
    raw_id_fields = ['user']
    readonly_fields = ['book_count', 'created_at', 'updated_at']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [CollectionItemInline]
    date_hierarchy = 'created_at'


@admin.register(CollectionItem)
class CollectionItemAdmin(admin.ModelAdmin):
    list_display = ['collection', 'book', 'order', 'added_at']
    list_filter = ['added_at']
    search_fields = ['collection__name', 'book__title']
    raw_id_fields = ['collection', 'book']
    date_hierarchy = 'added_at'
