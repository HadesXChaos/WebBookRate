from django.urls import path
from .views import (
    ReviewListView, ReviewDetailView, review_like_view,
    CommentListView, CommentDetailView, comment_like_view,
    ReviewByBookView,
)

app_name = 'reviews'

urlpatterns = [
    # Reviews
    path('', ReviewListView.as_view(), name='review_list'),
    path('write/', ReviewByBookView.as_view(), name='reviews_by_book'),
    path('<int:pk>/', ReviewDetailView.as_view(), name='review_detail'),
    path('<int:pk>/like/', review_like_view, name='review_like'),


    
    # Comments
    path('comments/', CommentListView.as_view(), name='comment_list'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment_detail'),
    path('comments/<int:pk>/like/', comment_like_view, name='comment_like'),
]
