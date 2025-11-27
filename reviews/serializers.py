from rest_framework import serializers
from django.conf import settings
from .models import Review, ReviewImage, Comment, Like
from books.models import Book
from books.serializers import BookListSerializer
from users.serializers import UserSerializer

# 1. ReviewImageSerializer (Độc lập)
class ReviewImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewImage
        fields = ['id', 'image', 'caption', 'order']
        read_only_fields = ['id']

# 2. ReviewSerializer (CHÍNH - Dùng để ghi)
class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    book_info = BookListSerializer(source='book', read_only=True)
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), write_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'book', 'book_info', 'title', 'body_md', 'body_html', 'rating', 'status', 'like_count', 'comment_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'body_html', 'like_count', 'comment_count', 'created_at', 'updated_at', 'book_info']

    def validate(self, attrs):
        request = self.context.get('request')
        if request and request.method == 'POST':
            user = request.user
            book = attrs.get('book')
            if Review.objects.filter(user=user, book=book).exists():
                raise serializers.ValidationError({"detail": "Bạn đã review cuốn sách này rồi."})
        return attrs

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

# 3. ReviewListSerializer (Dùng để đọc)
class ReviewListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    book = BookListSerializer(read_only=True)
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Review
        fields = ['id', 'book', 'user', 'title', 'body_html', 'rating', 'like_count', 'comment_count', 'is_liked', 'created_at', 'updated_at', 'edited_at']

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Like.objects.filter(user=request.user, content_type__model='review', object_id=obj.id).exists()
        return False

# 4. ReviewDetailSerializer (Dùng để đọc chi tiết)
class ReviewDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    book = BookListSerializer(read_only=True)
    images = ReviewImageSerializer(many=True, read_only=True)
    is_liked = serializers.SerializerMethodField()
    user_can_edit = serializers.SerializerMethodField()
    
    class Meta:
        model = Review
        fields = ['id', 'book', 'user', 'title', 'body_md', 'body_html', 'rating', 'status', 'like_count', 'comment_count', 'images', 'is_liked', 'user_can_edit', 'created_at', 'updated_at', 'edited_at']

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Like.objects.filter(user=request.user, content_type__model='review', object_id=obj.id).exists()
        return False

    def get_user_can_edit(self, obj):
        request = self.context.get('request')
        return request and request.user == obj.user

# 5. CommentSerializer (Đặt ở đây, không import từ chính file này)
class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    user_can_edit = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ['id', 'review', 'user', 'parent', 'body', 'status', 'like_count', 'replies', 'is_liked', 'user_can_edit', 'created_at', 'updated_at']
        read_only_fields = ['id', 'like_count', 'created_at', 'updated_at']

    def get_replies(self, obj):
        if obj.is_reply(): return []
        replies = Comment.objects.filter(parent=obj, status='public', is_active=True)
        return CommentSerializer(replies, many=True, context=self.context).data

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Like.objects.filter(user=request.user, content_type__model='comment', object_id=obj.id).exists()
        return False

    def get_user_can_edit(self, obj):
        request = self.context.get('request')
        return request and request.user == obj.user

# 6. LikeSerializer
class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Like
        fields = ['id', 'user', 'created_at']