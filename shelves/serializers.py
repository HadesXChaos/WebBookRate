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

    class Meta:
        model = Shelf
        fields = ['id', 'user', 'name', 'system_type', 'description', 'visibility',
                 'cover_image', 'book_count', 'items', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'book_count', 'created_at', 'updated_at']


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
