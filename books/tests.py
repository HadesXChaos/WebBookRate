"""
Tests for books app
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

from .models import Book, Author, Genre, Publisher, Tag

User = get_user_model()


class BookModelTest(TestCase):
    """Test Book model"""
    
    def setUp(self):
        self.author = Author.objects.create(name='Test Author')
        self.genre = Genre.objects.create(name='Test Genre')
        self.publisher = Publisher.objects.create(name='Test Publisher')
        self.book = Book.objects.create(
            title='Test Book',
            description='Test Description',
            year=2023,
            pages=300,
            publisher=self.publisher
        )
        self.book.authors.add(self.author)
        self.book.genres.add(self.genre)
    
    def test_book_creation(self):
        """Test book creation"""
        self.assertEqual(self.book.title, 'Test Book')
        self.assertEqual(self.book.year, 2023)
        self.assertEqual(self.book.pages, 300)
        self.assertEqual(self.book.publisher, self.publisher)
        self.assertIn(self.author, self.book.authors.all())
        self.assertIn(self.genre, self.book.genres.all())
    
    def test_book_slug(self):
        """Test book slug generation"""
        self.assertEqual(self.book.slug, 'test-book')
    
    def test_book_str(self):
        """Test book string representation"""
        self.assertEqual(str(self.book), 'Test Book')
    
    def test_book_get_absolute_url(self):
        """Test book absolute URL"""
        url = self.book.get_absolute_url()
        self.assertIn('test-book', url)


class AuthorModelTest(TestCase):
    """Test Author model"""
    
    def setUp(self):
        self.author = Author.objects.create(
            name='Test Author',
            bio='Test Biography'
        )
    
    def test_author_creation(self):
        """Test author creation"""
        self.assertEqual(self.author.name, 'Test Author')
        self.assertEqual(self.author.bio, 'Test Biography')
        self.assertTrue(self.author.is_active)
    
    def test_author_slug(self):
        """Test author slug generation"""
        self.assertEqual(self.author.slug, 'test-author')
    
    def test_author_str(self):
        """Test author string representation"""
        self.assertEqual(str(self.author), 'Test Author')


class GenreModelTest(TestCase):
    """Test Genre model"""
    
    def setUp(self):
        self.genre = Genre.objects.create(
            name='Test Genre',
            description='Test Description'
        )
    
    def test_genre_creation(self):
        """Test genre creation"""
        self.assertEqual(self.genre.name, 'Test Genre')
        self.assertEqual(self.genre.description, 'Test Description')
        self.assertTrue(self.genre.is_active)
    
    def test_genre_slug(self):
        """Test genre slug generation"""
        self.assertEqual(self.genre.slug, 'test-genre')


class BookAPITest(APITestCase):
    """Test Book API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!'
        )
        self.token = Token.objects.create(user=self.user)
        self.author = Author.objects.create(name='Test Author')
        self.genre = Genre.objects.create(name='Test Genre')
        self.publisher = Publisher.objects.create(name='Test Publisher')
        self.book = Book.objects.create(
            title='Test Book',
            description='Test Description',
            year=2023,
            pages=300,
            publisher=self.publisher
        )
        self.book.authors.add(self.author)
        self.book.genres.add(self.genre)
    
    def test_list_books(self):
        """Test list books"""
        url = reverse('books:book_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)
    
    def test_get_book_detail(self):
        """Test get book detail"""
        url = reverse('books:book_detail', kwargs={'slug': self.book.slug})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Book')
        self.assertEqual(response.data['year'], 2023)
    
    def test_list_authors(self):
        """Test list authors"""
        url = reverse('books:author_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
    
    def test_list_genres(self):
        """Test list genres"""
        url = reverse('books:genre_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
    
    def test_list_publishers(self):
        """Test list publishers"""
        url = reverse('books:publisher_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
    
    def test_list_tags(self):
        """Test list tags"""
        url = reverse('books:tag_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

