from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    """
    Custom permission to only allow moderators.
    """

    def has_permission(self, request, view):
        # Check if user is staff or in Moderators group
        return (
            request.user and
            request.user.is_authenticated and
            (request.user.is_staff or request.user.groups.filter(name='Moderators').exists())
        )
