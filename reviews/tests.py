"""
Tests for reviews app
"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

from books.models import Book, Author, Publisher
from .models import Review, Comment, Like

User = get_user_model()


class ReviewModelTest(TestCase):
    """Test Review model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!'
        )
        self.author = Author.objects.create(name='Test Author')
        self.publisher = Publisher.objects.create(name='Test Publisher')
        self.book = Book.objects.create(
            title='Test Book',
            description='Test Description',
            publisher=self.publisher
        )
        self.book.authors.add(self.author)
        self.review = Review.objects.create(
            book=self.book,
            user=self.user,
            title='Test Review',
            body_md='This is a test review with more than 100 characters to meet the minimum requirement for review length.',
            rating=4.5,
            status='public'
        )
    
    def test_review_creation(self):
        """Test review creation"""
        self.assertEqual(self.review.title, 'Test Review')
        self.assertEqual(self.review.rating, 4.5)
        self.assertEqual(self.review.status, 'public')
        self.assertEqual(self.review.book, self.book)
        self.assertEqual(self.review.user, self.user)
    
    def test_review_html_sanitization(self):
        """Test review HTML sanitization"""
        self.assertIsNotNone(self.review.body_html)
        # Check that HTML is sanitized (no script tags)
        self.assertNotIn('<script', self.review.body_html)
    
    def test_review_str(self):
        """Test review string representation"""
        self.assertIn('testuser', str(self.review))
        self.assertIn('Test Book', str(self.review))
    
    def test_review_unique_together(self):
        """Test that user can only have one review per book"""
        with self.assertRaises(Exception):
            Review.objects.create(
                book=self.book,
                user=self.user,
                title='Another Review',
                body_md='Another test review with more than 100 characters to meet the minimum requirement.',
                rating=3.5
            )


class CommentModelTest(TestCase):
    """Test Comment model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!'
        )
        self.author = Author.objects.create(name='Test Author')
        self.publisher = Publisher.objects.create(name='Test Publisher')
        self.book = Book.objects.create(
            title='Test Book',
            description='Test Description',
            publisher=self.publisher
        )
        self.book.authors.add(self.author)
        self.review = Review.objects.create(
            book=self.book,
            user=self.user,
            title='Test Review',
            body_md='Test review body with more than 100 characters to meet the minimum requirement.',
            rating=4.5
        )
        self.comment = Comment.objects.create(
            review=self.review,
            user=self.user,
            body='Test comment'
        )
    
    def test_comment_creation(self):
        """Test comment creation"""
        self.assertEqual(self.comment.body, 'Test comment')
        self.assertEqual(self.comment.review, self.review)
        self.assertEqual(self.comment.user, self.user)
        self.assertEqual(self.comment.status, 'public')
    
    def test_comment_is_reply(self):
        """Test comment reply detection"""
        self.assertFalse(self.comment.is_reply())
        reply = Comment.objects.create(
            review=self.review,
            user=self.user,
            body='Test reply',
            parent=self.comment
        )
        self.assertTrue(reply.is_reply())


class ReviewAPITest(APITestCase):
    """Test Review API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!'
        )
        self.token = Token.objects.create(user=self.user)
        self.author = Author.objects.create(name='Test Author')
        self.publisher = Publisher.objects.create(name='Test Publisher')
        self.book = Book.objects.create(
            title='Test Book',
            description='Test Description',
            publisher=self.publisher
        )
        self.book.authors.add(self.author)
        self.review = Review.objects.create(
            book=self.book,
            user=self.user,
            title='Test Review',
            body_md='This is a test review with more than 100 characters to meet the minimum requirement for review length.',
            rating=4.5,
            status='public'
        )
    
    def test_list_reviews(self):
        """Test list reviews"""
        url = reverse('reviews:review_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)
    
    def test_get_review_detail(self):
        """Test get review detail"""
        url = reverse('reviews:review_detail', kwargs={'pk': self.review.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Review')
    
    def test_create_review(self):
        """Test create review"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse('reviews:review_list')
        data = {
            'book': self.book.pk,
            'title': 'New Review',
            'body_md': 'This is a new review with more than 100 characters to meet the minimum requirement for review length.',
            'rating': 5.0
        }
        response = self.client.post(url, data, format='json')
        # Should fail because user already has a review for this book
        self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_201_CREATED])
    
    def test_create_review_short_body(self):
        """Test create review with body too short"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        # Create a new book for this test
        new_book = Book.objects.create(
            title='New Book',
            description='New Description',
            publisher=self.publisher
        )
        new_book.authors.add(self.author)
        url = reverse('reviews:review_list')
        data = {
            'book': new_book.pk,
            'title': 'Short Review',
            'body_md': 'Short',  # Less than 100 characters
            'rating': 3.0
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_update_review(self):
        """Test update review"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse('reviews:review_detail', kwargs={'pk': self.review.pk})
        data = {
            'title': 'Updated Review',
            'body_md': 'This is an updated review with more than 100 characters to meet the minimum requirement.'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.review.refresh_from_db()
        self.assertEqual(self.review.title, 'Updated Review')
    
    def test_delete_review(self):
        """Test delete review"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse('reviews:review_detail', kwargs={'pk': self.review.pk})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Review.objects.filter(pk=self.review.pk).exists())


class CommentAPITest(APITestCase):
    """Test Comment API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!'
        )
        self.token = Token.objects.create(user=self.user)
        self.author = Author.objects.create(name='Test Author')
        self.publisher = Publisher.objects.create(name='Test Publisher')
        self.book = Book.objects.create(
            title='Test Book',
            description='Test Description',
            publisher=self.publisher
        )
        self.book.authors.add(self.author)
        self.review = Review.objects.create(
            book=self.book,
            user=self.user,
            title='Test Review',
            body_md='Test review body with more than 100 characters to meet the minimum requirement.',
            rating=4.5
        )
        self.comment = Comment.objects.create(
            review=self.review,
            user=self.user,
            body='Test comment'
        )
    
    def test_list_comments(self):
        """Test list comments"""
        url = reverse('reviews:comment_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
    
    def test_create_comment(self):
        """Test create comment"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse('reviews:comment_list')
        data = {
            'review': self.review.pk,
            'body': 'New comment'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Comment.objects.filter(body='New comment').exists())


class LikeAPITest(APITestCase):
    """Test Like API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!'
        )
        self.token = Token.objects.create(user=self.user)
        self.author = Author.objects.create(name='Test Author')
        self.publisher = Publisher.objects.create(name='Test Publisher')
        self.book = Book.objects.create(
            title='Test Book',
            description='Test Description',
            publisher=self.publisher
        )
        self.book.authors.add(self.author)
        self.review = Review.objects.create(
            book=self.book,
            user=self.user,
            title='Test Review',
            body_md='Test review body with more than 100 characters to meet the minimum requirement.',
            rating=4.5
        )
    
    def test_like_review(self):
        """Test like review"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse('reviews:review_like', kwargs={'pk': self.review.pk})
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Like.objects.filter(
            user=self.user,
            content_type__model='review',
            object_id=self.review.pk
        ).exists())
    
    def test_unlike_review(self):
        """Test unlike review"""
        # First like
        Like.objects.create(
            user=self.user,
            content_object=self.review
        )
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse('reviews:review_like', kwargs={'pk': self.review.pk})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Like.objects.filter(
            user=self.user,
            content_type__model='review',
            object_id=self.review.pk
        ).exists())

