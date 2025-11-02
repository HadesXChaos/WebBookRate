from django.contrib import admin
from .models import Shelf, ShelfItem, ReadingProgress


class ShelfItemInline(admin.TabularInline):
    model = ShelfItem
    extra = 1
    raw_id_fields = ['book']


@admin.register(Shelf)
class ShelfAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'system_type', 'visibility', 'book_count', 
                   'is_active', 'created_at']
    list_filter = ['system_type', 'visibility', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'user__username']
    raw_id_fields = ['user']
    readonly_fields = ['book_count', 'created_at', 'updated_at']
    inlines = [ShelfItemInline]
    date_hierarchy = 'created_at'


@admin.register(ShelfItem)
class ShelfItemAdmin(admin.ModelAdmin):
    list_display = ['shelf', 'book', 'order', 'added_at']
    list_filter = ['added_at']
    search_fields = ['shelf__name', 'book__title']
    raw_id_fields = ['shelf', 'book']
    date_hierarchy = 'added_at'


@admin.register(ReadingProgress)
class ReadingProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'page', 'percent', 'updated_at']
    list_filter = ['updated_at']
    search_fields = ['user__username', 'book__title']
    raw_id_fields = ['user', 'book']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'updated_at'
