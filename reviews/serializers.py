from rest_framework import serializers
from django.conf import settings
from .models import Review, ReviewImage, Comment, Like
from books.serializers import BookListSerializer
from users.serializers import UserSerializer


class ReviewImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewImage
        fields = ['id', 'image', 'caption', 'order']
        read_only_fields = ['id']


class ReviewListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list view"""
    user = UserSerializer(read_only=True)
    book = BookListSerializer(read_only=True)
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Review
        fields = ['id', 'book', 'user', 'title', 'body_html', 'rating', 
                 'like_count', 'comment_count', 'is_liked', 'created_at', 
                 'updated_at', 'edited_at']
        read_only_fields = ['id', 'body_html', 'like_count', 'comment_count', 
                           'created_at', 'updated_at', 'edited_at']

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Like.objects.filter(
                user=request.user,
                content_type__model='review',
                object_id=obj.id
            ).exists()
        return False


class ReviewDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for detail view"""
    user = UserSerializer(read_only=True)
    book = BookListSerializer(read_only=True)
    images = ReviewImageSerializer(many=True, read_only=True)
    is_liked = serializers.SerializerMethodField()
    user_can_edit = serializers.SerializerMethodField()
    
    class Meta:
        model = Review
        fields = ['id', 'book', 'user', 'title', 'body_md', 'body_html', 
                 'rating', 'status', 'like_count', 'comment_count', 'images',
                 'is_liked', 'user_can_edit', 'created_at', 'updated_at', 
                 'edited_at']
        read_only_fields = ['id', 'body_html', 'like_count', 'comment_count', 
                           'created_at', 'updated_at', 'edited_at']

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Like.objects.filter(
                user=request.user,
                content_type__model='review',
                object_id=obj.id
            ).exists()
        return False

    def get_user_can_edit(self, obj):
        request = self.context.get('request')
        return request and request.user == obj.user

    def validate_body_md(self, value):
        if len(value) < settings.REVIEW_MIN_LENGTH:
            raise serializers.ValidationError(
                f"Review must be at least {settings.REVIEW_MIN_LENGTH} characters."
            )
        return value


class CommentSerializer(serializers.ModelSerializer):
    """Comment Serializer"""
    user = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    user_can_edit = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ['id', 'review', 'user', 'parent', 'body', 'status', 
                 'like_count', 'replies', 'is_liked', 'user_can_edit',
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'like_count', 'created_at', 'updated_at']

    def get_replies(self, obj):
        if obj.is_reply():
            return []
        replies = Comment.objects.filter(parent=obj, status='public', is_active=True)
        return CommentSerializer(replies, many=True, context=self.context).data

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Like.objects.filter(
                user=request.user,
                content_type__model='comment',
                object_id=obj.id
            ).exists()
        return False

    def get_user_can_edit(self, obj):
        request = self.context.get('request')
        return request and request.user == obj.user


class LikeSerializer(serializers.ModelSerializer):
    """Like Serializer"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Like
        fields = ['id', 'user', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
