from rest_framework import serializers
from .models import Author, Genre, Publisher, Tag, Book, BookEdition


class AuthorSerializer(serializers.ModelSerializer):
    book_count = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = ['id', 'name', 'slug', 'bio', 'photo', 'birth_date', 
                 'death_date', 'nationality', 'website', 'book_count']
        read_only_fields = ['id', 'slug', 'book_count']

    def get_book_count(self, obj):
        return obj.books.filter(is_active=True).count()


class GenreSerializer(serializers.ModelSerializer):
    book_count = serializers.SerializerMethodField()

    class Meta:
        model = Genre
        fields = ['id', 'name', 'slug', 'description', 'parent', 'book_count']
        read_only_fields = ['id', 'slug', 'book_count']

    def get_book_count(self, obj):
        return obj.books.filter(is_active=True).count()


class PublisherSerializer(serializers.ModelSerializer):
    book_count = serializers.SerializerMethodField()

    class Meta:
        model = Publisher
        fields = ['id', 'name', 'slug', 'description', 'logo', 'website', 'book_count']
        read_only_fields = ['id', 'slug', 'book_count']

    def get_book_count(self, obj):
        return obj.books.filter(is_active=True).count()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'description']
        read_only_fields = ['id', 'slug']


class BookEditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookEdition
        fields = ['id', 'isbn13', 'format', 'published_at', 'language', 'pages']
        read_only_fields = ['id']


class BookListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list view"""
    authors = AuthorSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    primary_genre = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'slug', 'cover', 'year', 'authors', 
                 'genres', 'primary_genre', 'avg_rating', 'rating_count', 
                 'review_count']
        read_only_fields = ['id', 'slug']

    def get_primary_genre(self, obj):
        primary = obj.genres.first()
        if primary:
            return GenreSerializer(primary).data
        return None


class BookDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for detail view"""
    authors = AuthorSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    publisher = PublisherSerializer(read_only=True)
    editions = BookEditionSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'slug', 'description', 'cover', 'year', 
                 'pages', 'language', 'publisher', 'authors', 'genres', 
                 'tags', 'editions', 'avg_rating', 'rating_count', 
                 'review_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'slug', 'avg_rating', 'rating_count', 
                          'review_count', 'created_at', 'updated_at']
