from rest_framework import serializers
from .models import Follow, Notification, Collection, CollectionItem
from books.serializers import BookListSerializer
from users.serializers import UserSerializer


class FollowSerializer(serializers.ModelSerializer):
    follower = UserSerializer(read_only=True)
    target = serializers.SerializerMethodField()
    target_type = serializers.CharField(write_only=True, required=False)
    target_id = serializers.IntegerField(write_only=True, required=False, source='object_id')

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'target_type', 'target_id', 'target', 'created_at']
        read_only_fields = ['id', 'follower', 'target', 'created_at']

    def get_target(self, obj):
        """Serialize the target object based on content type"""
        target = obj.target
        if not target:
            return None
        
        # Serialize based on content type model
        if obj.content_type.model == 'user':
            return UserSerializer(target).data
        elif obj.content_type.model == 'author':
            from books.serializers import AuthorSerializer
            return AuthorSerializer(target).data
        elif obj.content_type.model == 'book':
            return BookListSerializer(target).data
        return None

    def create(self, validated_data):
        """Create a Follow instance from target_type and target_id"""
        from django.contrib.contenttypes.models import ContentType
        
        target_type = validated_data.pop('target_type', None)
        object_id = validated_data.pop('object_id', None)
        
        if target_type and object_id:
            # Get ContentType from model name
            try:
                content_type = ContentType.objects.get(model=target_type)
                validated_data['content_type'] = content_type
                validated_data['object_id'] = object_id
            except ContentType.DoesNotExist:
                raise serializers.ValidationError(
                    {'target_type': f'Invalid target type: {target_type}'}
                )
        
        return super().create(validated_data)
    
    def to_representation(self, instance):
        """Add target_type to representation"""
        ret = super().to_representation(instance)
        ret['target_type'] = instance.content_type.model if instance.content_type else None
        return ret


class NotificationSerializer(serializers.ModelSerializer):
    content_object = serializers.SerializerMethodField()
    message = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'notification_type', 'message', 'content_object',
                  'payload', 'url', 'is_read', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_message(self, obj):
        if isinstance(obj.payload, dict):
            return obj.payload.get('message')
        return None

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
    
    def get_url(self, obj):
        """
        Tạo URL để frontend redirect khi click vào notification
        - Nếu payload có 'url' thì ưu tiên dùng luôn
        - Nếu content_type là review/comment/user thì tự build URL tương ứng
        """
        from django.urls import reverse

        # Nếu payload đã có url thì trả về luôn (để sau này dễ custom)
        if isinstance(obj.payload, dict) and obj.payload.get('url'):
            return obj.payload['url']

        if not obj.content_type:
            return None

        model_name = obj.content_type.model

        try:
            # 1) Thông báo liên quan tới REVIEW (new_review, review_like, v.v.)
            if model_name == 'review':
                review = obj.content_object
                if review:
                    # Frontend xem review: /reviews/<pk>/
                    return reverse('review_detail_frontend', args=[review.pk])

            # 2) Thông báo liên quan tới COMMENT (review_comment, comment_reply, comment_like)
            if model_name == 'comment':
                comment = obj.content_object
                if comment:
                    # Nhảy tới trang review và cuộn tới khu vực comment
                    return reverse('review_detail_frontend', args=[comment.review_id]) + '#comments'

            # 3) Thông báo follow: content_object là USER (người follow mình)
            if model_name == 'user':
                user = obj.content_object
                if user:
                    # Trang profile frontend: /users/<username>/
                    return reverse('user_profile', args=[user.username])

        except Exception:
            # Không để API toang nếu có lỗi build URL
            return None

        return None


class CollectionItemSerializer(serializers.ModelSerializer):
    book = BookListSerializer(read_only=True)

    class Meta:
        model = CollectionItem
        fields = ['id', 'book', 'notes', 'order', 'added_at']
        read_only_fields = ['id', 'added_at']


class CollectionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    items = CollectionItemSerializer(many=True, read_only=True)

    class Meta:
        model = Collection
        fields = ['id', 'user', 'name', 'slug', 'description', 'cover_image',
                 'visibility', 'book_count', 'items', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'slug', 'book_count', 'created_at', 'updated_at']
