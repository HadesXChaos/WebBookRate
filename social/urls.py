from django.urls import path
from .views import (
    FollowToggleView,
    NotificationListView, mark_notification_read, mark_all_notifications_read,
    CollectionListView, CollectionDetailView, collection_item_view,
    feed_view,
)

app_name = 'social'

urlpatterns = [
    # Follow / Unfollow
    path('follow/', FollowToggleView.as_view(), name='follow-toggle'),
    
    # Notifications
    path('notifications/', NotificationListView.as_view(), name='notification_list'),
    path('notifications/<int:pk>/read/', mark_notification_read, name='notification_read'),
    path('notifications/read-all/', mark_all_notifications_read, name='notification_read_all'),
    
    # Collections
    path('collections/', CollectionListView.as_view(), name='collection_list'),
    path('collections/<int:pk>/', CollectionDetailView.as_view(), name='collection_detail'),
    path('collections/<int:collection_id>/books/<int:book_id>/', collection_item_view, name='collection_item'),
    
    # Feed
    path('feed/', feed_view, name='feed'),
]
