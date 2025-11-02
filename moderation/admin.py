from django.contrib import admin
from .models import Report, ModeratorAction


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'reporter', 'content_type', 'object_id', 'reason', 
                   'status', 'moderator', 'created_at']
    list_filter = ['status', 'reason', 'created_at']
    search_fields = ['reporter__username', 'note', 'moderator_note']
    raw_id_fields = ['reporter', 'moderator']
    readonly_fields = ['created_at', 'updated_at', 'resolved_at']
    date_hierarchy = 'created_at'


@admin.register(ModeratorAction)
class ModeratorActionAdmin(admin.ModelAdmin):
    list_display = ['moderator', 'action', 'content_type', 'object_id', 
                   'report', 'created_at']
    list_filter = ['action', 'created_at']
    search_fields = ['moderator__username', 'note']
    raw_id_fields = ['moderator', 'report']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
