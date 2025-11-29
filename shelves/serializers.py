from rest_framework import serializers
from .models import Shelf, ShelfItem, ReadingProgress
from books.serializers import BookListSerializer
from users.serializers import UserSerializer


class ShelfItemSerializer(serializers.ModelSerializer):
    book = BookListSerializer(read_only=True)

    class Meta:
        model = ShelfItem
        fields = ['id', 'book', 'order', 'added_at']
        read_only_fields = ['id', 'added_at']


class ShelfSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    items = ShelfItemSerializer(many=True, read_only=True)
    has_book = serializers.BooleanField(read_only=True, required=False)
    book_count = serializers.SerializerMethodField()

    class Meta:
        model = Shelf
        fields = ['id', 'user', 'name', 'system_type', 'description', 'visibility',
                 'cover_image', 'book_count', 'items', 'created_at', 'updated_at', 'has_book']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

        extra_kwargs = {
            'system_type': {'required': False, 'allow_null': True}
        }
    
    def get_book_count(self, obj):
        # Use annotated count if available, otherwise use model field or count items
        if hasattr(obj, 'annotated_book_count'):
            return obj.annotated_book_count
        elif hasattr(obj, 'book_count') and obj.book_count is not None:
            return obj.book_count
        elif hasattr(obj, 'items'):
            return obj.items.count()
        return 0

    


class ReadingProgressSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    book = BookListSerializer(read_only=True)

    class Meta:
        model = ReadingProgress
        fields = ['id', 'user', 'book', 'page', 'percent', 'notes', 
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def validate(self, attrs):
        book = attrs.get('book') or (self.instance and self.instance.book)
        page = attrs.get('page')
        percent = attrs.get('percent')
        
        if page and book and book.pages and page > book.pages:
            raise serializers.ValidationError(
                {'page': 'Page cannot exceed total pages of the book.'}
            )
        if percent and (percent < 0 or percent > 100):
            raise serializers.ValidationError(
                {'percent': 'Percent must be between 0 and 100.'}
            )
        
        return attrs
