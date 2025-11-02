from django.urls import path
from .views import (
    ReportListView, ReportDetailView, resolve_report,
    ModeratorActionListView,
)

app_name = 'moderation'

urlpatterns = [
    path('reports/', ReportListView.as_view(), name='report_list'),
    path('reports/<int:pk>/', ReportDetailView.as_view(), name='report_detail'),
    path('reports/<int:pk>/resolve/', resolve_report, name='resolve_report'),
    path('actions/', ModeratorActionListView.as_view(), name='action_list'),
]
