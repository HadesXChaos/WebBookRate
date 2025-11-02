from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from .models import Report, ModeratorAction
from .serializers import ReportSerializer, ModeratorActionSerializer
from .permissions import IsModerator


class ReportListView(generics.ListCreateAPIView):
    """Report List and Create"""
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        # Moderators can see all reports
        if user.is_staff or user.groups.filter(name='Moderators').exists():
            status_filter = self.request.query_params.get('status', 'pending')
            return Report.objects.filter(status=status_filter).order_by('-created_at')
        
        # Regular users can only see their own reports
        return Report.objects.filter(reporter=user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)


class ReportDetailView(generics.RetrieveAPIView):
    """Report Detail"""
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        # Moderators can see all reports
        if user.is_staff or user.groups.filter(name='Moderators').exists():
            return Report.objects.all()
        
        # Regular users can only see their own reports
        return Report.objects.filter(reporter=user)


@api_view(['POST'])
@permission_classes([IsModerator])
def resolve_report(request, pk):
    """Resolve Report - Moderator only"""
    report = get_object_or_404(Report, pk=pk)
    
    action_type = request.data.get('action')
    note = request.data.get('note', '')
    
    if action_type == 'approve':
        # Reject the report
        report.status = 'rejected'
        report.moderator = request.user
        report.moderator_note = note
        report.resolved_at = timezone.now()
        report.save()
        
    elif action_type == 'reject':
        # Reject the report
        report.status = 'rejected'
        report.moderator = request.user
        report.moderator_note = note
        report.resolved_at = timezone.now()
        report.save()
        
    elif action_type == 'hide':
        # Hide the content
        content_obj = report.content_object
        if hasattr(content_obj, 'is_active'):
            content_obj.is_active = False
            content_obj.save()
        elif hasattr(content_obj, 'status'):
            content_obj.status = 'hidden'
            content_obj.save()
        
        # Create moderator action
        ModeratorAction.objects.create(
            moderator=request.user,
            action='hide',
            content_type=report.content_type,
            object_id=report.object_id,
            report=report,
            note=note
        )
        
        report.status = 'resolved'
        report.moderator = request.user
        report.moderator_note = note
        report.resolved_at = timezone.now()
        report.save()
        
    elif action_type == 'delete':
        # Delete the content
        content_obj = report.content_object
        if hasattr(content_obj, 'delete'):
            content_obj.delete()
        
        # Create moderator action
        ModeratorAction.objects.create(
            moderator=request.user,
            action='delete',
            content_type=report.content_type,
            object_id=report.object_id,
            report=report,
            note=note
        )
        
        report.status = 'resolved'
        report.moderator = request.user
        report.moderator_note = note
        report.resolved_at = timezone.now()
        report.save()
    
    return Response(ReportSerializer(report).data)


class ModeratorActionListView(generics.ListAPIView):
    """Moderator Action List - Moderator only"""
    queryset = ModeratorAction.objects.all().order_by('-created_at')
    serializer_class = ModeratorActionSerializer
    permission_classes = [IsModerator]
