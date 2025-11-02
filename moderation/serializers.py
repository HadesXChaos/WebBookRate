from rest_framework import serializers
from .models import Report, ModeratorAction
from users.serializers import UserSerializer


class ReportSerializer(serializers.ModelSerializer):
    reporter = UserSerializer(read_only=True)
    moderator = UserSerializer(read_only=True)
    content_object = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = ['id', 'reporter', 'content_type', 'object_id', 'content_object',
                 'reason', 'note', 'status', 'moderator', 'moderator_note',
                 'created_at', 'updated_at', 'resolved_at']
        read_only_fields = ['id', 'reporter', 'status', 'moderator', 'moderator_note',
                           'created_at', 'updated_at', 'resolved_at']

    def get_content_object(self, obj):
        if obj.content_object:
            # Serialize based on content type
            if obj.content_type.model == 'review':
                from reviews.serializers import ReviewListSerializer
                return ReviewListSerializer(obj.content_object, context=self.context).data
            elif obj.content_type.model == 'comment':
                from reviews.serializers import CommentSerializer
                return CommentSerializer(obj.content_object, context=self.context).data
        return None


class ModeratorActionSerializer(serializers.ModelSerializer):
    moderator = UserSerializer(read_only=True)
    content_object = serializers.SerializerMethodField()

    class Meta:
        model = ModeratorAction
        fields = ['id', 'moderator', 'action', 'content_type', 'object_id', 
                 'content_object', 'report', 'note', 'created_at']
        read_only_fields = ['id', 'moderator', 'created_at']

    def get_content_object(self, obj):
        if obj.content_object:
            # Serialize based on content type
            if obj.content_type.model == 'review':
                from reviews.serializers import ReviewListSerializer
                return ReviewListSerializer(obj.content_object, context=self.context).data
            elif obj.content_type.model == 'comment':
                from reviews.serializers import CommentSerializer
                return CommentSerializer(obj.content_object, context=self.context).data
        return None
