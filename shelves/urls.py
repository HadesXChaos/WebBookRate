from django.urls import path
from .views import (
    ShelfListView, ShelfDetailView, shelf_item_view,
    ReadingProgressListView, ReadingProgressDetailView,
    UserShelvesView,
)

app_name = 'shelves'

urlpatterns = [
    # Shelves
    path('', ShelfListView.as_view(), name='shelf_list'),
    path('<int:pk>/', ShelfDetailView.as_view(), name='shelf_detail'),
    path('<int:shelf_id>/books/<int:book_id>/', shelf_item_view, name='shelf_item'),
    path('users/<str:username>/', UserShelvesView.as_view(), name='user_shelves'),
    
    # Reading Progress
    path('progress/', ReadingProgressListView.as_view(), name='progress_list'),
    path('progress/<int:pk>/', ReadingProgressDetailView.as_view(), name='progress_detail'),
]
