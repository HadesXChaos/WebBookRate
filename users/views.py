from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from django.utils import timezone
from datetime import timedelta
import secrets

from .models import User, Profile, EmailVerification
from .serializers import UserSerializer, ProfileSerializer, RegisterSerializer, LoginSerializer


class RegisterView(generics.CreateAPIView):
    """User Registration"""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Create email verification token
        token = secrets.token_urlsafe(32)
        EmailVerification.objects.create(
            user=user,
            token=token,
            expires_at=timezone.now() + timedelta(days=7)
        )
        
        # TODO: Send verification email
        
        return Response({
            'user': UserSerializer(user).data,
            'message': 'Registration successful. Please verify your email.'
        }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """User Login"""
    serializer = LoginSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    
    login(request, user)
    token, created = Token.objects.get_or_create(user=user)
    
    return Response({
        'token': token.key,
        'user': UserSerializer(user).data
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """User Logout"""
    try:
        request.user.auth_token.delete()
    except:
        pass
    return Response({'message': 'Logout successful'})


class ProfileView(generics.RetrieveUpdateAPIView):
    """User Profile"""
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile


class UserDetailView(generics.RetrieveAPIView):
    """Public User Profile"""
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [permissions.AllowAny]


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def verify_email(request, token):
    """Email Verification"""
    try:
        verification = EmailVerification.objects.get(
            token=token,
            is_used=False,
            expires_at__gt=timezone.now()
        )
        verification.user.is_verified = True
        verification.user.save()
        verification.is_used = True
        verification.save()
        return Response({'message': 'Email verified successfully'})
    except EmailVerification.DoesNotExist:
        return Response({'error': 'Invalid or expired token'}, 
                       status=status.HTTP_400_BAD_REQUEST)
