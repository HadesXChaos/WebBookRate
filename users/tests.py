"""
Tests for users app
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

from .models import Profile, EmailVerification, PasswordResetToken
from .validators import validate_password_strength
from django.core.exceptions import ValidationError

User = get_user_model()


class UserModelTest(TestCase):
    """Test User model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!'
        )
    
    def test_user_creation(self):
        """Test user creation"""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertFalse(self.user.is_verified)
        self.assertTrue(self.user.is_active)
    
    def test_user_str(self):
        """Test user string representation"""
        self.assertEqual(str(self.user), 'testuser')
    
    def test_profile_creation(self):
        """Test profile is created automatically"""
        profile, created = Profile.objects.get_or_create(user=self.user)
        self.assertTrue(created or profile.user == self.user)
        self.assertEqual(profile.user, self.user)


class PasswordValidatorTest(TestCase):
    """Test password strength validator"""
    
    def test_valid_password(self):
        """Test valid password passes validation"""
        password = 'TestPass123!'
        try:
            validate_password_strength(password)
        except ValidationError:
            self.fail("Valid password should not raise ValidationError")
    
    def test_short_password(self):
        """Test password too short"""
        password = 'Test1!'
        with self.assertRaises(ValidationError):
            validate_password_strength(password)
    
    def test_no_uppercase(self):
        """Test password without uppercase"""
        password = 'testpass123!'
        with self.assertRaises(ValidationError):
            validate_password_strength(password)
    
    def test_no_lowercase(self):
        """Test password without lowercase"""
        password = 'TESTPASS123!'
        with self.assertRaises(ValidationError):
            validate_password_strength(password)
    
    def test_no_digit(self):
        """Test password without digit"""
        password = 'TestPass!'
        with self.assertRaises(ValidationError):
            validate_password_strength(password)
    
    def test_no_special_char(self):
        """Test password without special character"""
        password = 'TestPass123'
        with self.assertRaises(ValidationError):
            validate_password_strength(password)


class UserAPITest(APITestCase):
    """Test User API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!'
        )
        self.token = Token.objects.create(user=self.user)
    
    def test_register_user(self):
        """Test user registration"""
        url = reverse('users:register')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'NewPass123!',
            'password_confirm': 'NewPass123!'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        # Check email verification token was created
        new_user = User.objects.get(username='newuser')
        self.assertTrue(EmailVerification.objects.filter(user=new_user).exists())
    
    def test_register_weak_password(self):
        """Test registration with weak password"""
        url = reverse('users:register')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'weak',
            'password_confirm': 'weak'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_login(self):
        """Test user login"""
        url = reverse('users:login')
        data = {
            'username': 'testuser',
            'password': 'TestPass123!'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        url = reverse('users:login')
        data = {
            'username': 'testuser',
            'password': 'WrongPass123!'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_logout(self):
        """Test user logout"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse('users:logout')
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_profile(self):
        """Test get user profile"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse('users:profile')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user', response.data)
    
    def test_update_profile(self):
        """Test update user profile"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse('users:profile')
        data = {
            'bio': 'Test bio',
            'location': 'Test Location'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.bio, 'Test bio')
        self.assertEqual(profile.location, 'Test Location')


class EmailVerificationTest(APITestCase):
    """Test email verification"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!'
        )
        self.verification = EmailVerification.objects.create(
            user=self.user,
            token='test-token-123',
            expires_at=timezone.now() + timedelta(days=7)
        )
    
    def test_verify_email(self):
        """Test email verification"""
        url = reverse('users:verify_email', kwargs={'token': 'test-token-123'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_verified)
        self.verification.refresh_from_db()
        self.assertTrue(self.verification.is_used)
    
    def test_verify_email_invalid_token(self):
        """Test email verification with invalid token"""
        url = reverse('verify_email', kwargs={'token': 'invalid-token'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_verify_email_expired_token(self):
        """Test email verification with expired token"""
        self.verification.expires_at = timezone.now() - timedelta(days=1)
        self.verification.save()
        url = reverse('users:verify_email', kwargs={'token': 'test-token-123'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PasswordResetTest(APITestCase):
    """Test password reset"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!'
        )
    
    def test_password_reset_request(self):
        """Test password reset request"""
        url = reverse('users:password_reset_request')
        data = {'email': 'test@example.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(PasswordResetToken.objects.filter(user=self.user).exists())
    
    def test_password_reset_confirm(self):
        """Test password reset confirmation"""
        token = PasswordResetToken.objects.create(
            user=self.user,
            token='reset-token-123',
            expires_at=timezone.now() + timedelta(hours=1)
        )
        url = reverse('users:password_reset_confirm')
        data = {
            'token': 'reset-token-123',
            'new_password': 'NewPass123!',
            'new_password_confirm': 'NewPass123!'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verify password was changed
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewPass123!'))
        token.refresh_from_db()
        self.assertTrue(token.is_used)
    
    def test_password_reset_invalid_token(self):
        """Test password reset with invalid token"""
        url = reverse('users:password_reset_confirm')
        data = {
            'token': 'invalid-token',
            'new_password': 'NewPass123!',
            'new_password_confirm': 'NewPass123!'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

