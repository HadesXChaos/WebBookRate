from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile, EmailVerification


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email','role', 'is_verified', 'is_staff', 'is_active', 'created_at']
    list_filter = ['role','is_staff', 'is_active', 'is_verified', 'created_at']
    search_fields = ['username', 'email']
    date_hierarchy = 'created_at'
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Thông tin bổ sung', {'fields': ('role', 'is_verified')}),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Thông tin bổ sung', {'fields': ('role', 'is_verified', 'email')}),
    )

    def get_queryset(self, request):
        """ Limit user visibility in admin based on role """
        qs = super().get_queryset(request)
        
        if request.user.is_superuser:
            return qs
        
        return qs.filter(
            is_superuser=False
        ).exclude(
            role='moderator'
        ) | qs.filter(pk=request.user.pk)

    def has_change_permission(self, request, obj=None):
        if not super().has_change_permission(request, obj):
            return False

        if request.user.is_superuser:
            return True

        if obj is None:
            return True

        if obj.is_superuser:
            return False
        
        if obj.role == User.Role.MODERATOR and obj != request.user:
            return False
            
        if obj.role == User.Role.ADMIN:
            return False

        return True

    def has_delete_permission(self, request, obj=None):
        """ Limit delete permission in admin based on role """
        if not super().has_delete_permission(request, obj):
            return False
            
        if request.user.is_superuser:
            return True
            
        if obj is None:
            return True

        if obj.is_superuser or obj.role in [User.Role.MODERATOR, User.Role.ADMIN]:
            return False
            
        return True

    def get_readonly_fields(self, request, obj=None):
        """ Make certain fields readonly based on user role """
        readonly_fields = super().get_readonly_fields(request, obj)
        
        if request.user.is_superuser:
            return readonly_fields
            
        sensitive_fields = [
            'is_superuser', 
            'is_staff', 
            'groups', 
            'user_permissions', 
            'last_login', 
            'date_joined'
        ]
        
        if obj == request.user:
            sensitive_fields.append('role')
            sensitive_fields.append('is_active')
            sensitive_fields.append('is_verified')
        
        return tuple(list(readonly_fields) + sensitive_fields)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'language', 'created_at']
    search_fields = ['user__username', 'user__email', 'bio']
    raw_id_fields = ['user']


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'token', 'is_used', 'created_at', 'expires_at']
    list_filter = ['is_used', 'created_at']
    search_fields = ['user__email', 'token']
    readonly_fields = ['token', 'created_at']
