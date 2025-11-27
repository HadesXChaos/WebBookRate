from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.db.utils import OperationalError, ProgrammingError
from .models import User


@receiver(post_migrate)
def create_moderator_group(sender, **kwargs):
    """ create 'Moderators' group with appropriate permissions after migrations """
    if sender.name != 'users':
        return

    try:
        group_name = 'Moderators'
        group, created = Group.objects.get_or_create(name=group_name)

        moderator_permissions = [
            'view_report', 'change_report',
            'add_moderatoraction', 'view_moderatoraction',
            'view_review', 'change_review', 'delete_review',
            'view_comment', 'change_comment', 'delete_comment',
            'view_reviewimage', 'change_reviewimage', 'delete_reviewimage',
            'view_book', 'add_book', 'change_book', 
            'view_author', 'add_author', 'change_author',
            'view_publisher', 'add_publisher', 'change_publisher',
            'view_genre', 'add_genre', 'change_genre',
            'view_tag', 'add_tag', 'change_tag',
            'view_user', 'change_user',
            'view_profile', 'change_profile',
            'view_collection', 'delete_collection',
        ]

        permissions_to_add = []
        for codename in moderator_permissions:
            try:
                perm = Permission.objects.get(codename=codename)
                permissions_to_add.append(perm)
            except Permission.DoesNotExist:
                continue

        group.permissions.set(permissions_to_add)
        
        
    except (OperationalError, ProgrammingError):
        pass



@receiver(post_save, sender=User)
def sync_user_role(sender, instance, created, **kwargs):
    """ Sync is_staff and Group membership based on User role """
    try:
        mod_group = Group.objects.get(name='Moderators')
    except Group.DoesNotExist:
        return

    if instance.role == User.Role.MODERATOR:
        if not instance.is_staff:
            instance.is_staff = True
            User.objects.filter(pk=instance.pk).update(is_staff=True)
        
        if mod_group not in instance.groups.all():
            instance.groups.add(mod_group)
            
    else:
        
        if mod_group in instance.groups.all():
            instance.groups.remove(mod_group)
            
        if not instance.is_superuser and instance.is_staff:
            instance.is_staff = False
            User.objects.filter(pk=instance.pk).update(is_staff=False)