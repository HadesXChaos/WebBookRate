from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.throttling import ScopedRateThrottle
from django.views.decorators.csrf import csrf_exempt 
from django.contrib.auth import login
from django.utils import timezone
from datetime import timedelta
import secrets

from .models import User, Profile, EmailVerification, PasswordResetToken
from .serializers import (
    UserSerializer, ProfileSerializer, RegisterSerializer, LoginSerializer,
    PasswordResetRequestSerializer, PasswordResetConfirmSerializer,ChangePasswordSerializer,
)
from .utils import send_verification_email, send_password_reset_email
from .throttles import RegisterThrottle, LoginThrottle, PasswordResetThrottle, EmailVerificationThrottle


class RegisterView(generics.CreateAPIView):
    """User Registration"""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [RegisterThrottle]

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
        
        # Send verification email
        send_verification_email(user, token)
        
        return Response({
            'user': UserSerializer(user).data,
            'message': 'Registration successful. Please verify your email.'
        }, status=status.HTTP_201_CREATED)

@csrf_exempt 
@api_view(['POST'])
@authentication_classes([])  
@permission_classes([permissions.AllowAny])
def login_view(request):
    """User Login"""
    # Apply throttle manually for function-based view
    throttle = LoginThrottle()
    if not throttle.allow_request(request, None):
        from rest_framework.exceptions import Throttled
        raise Throttled(detail="Too many login attempts. Please try again later.")
    
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


@api_view(['GET', 'POST'])
@permission_classes([permissions.AllowAny])
def verify_email(request, token):
    """Email Verification - Supports both GET (frontend) and POST (API)"""
    # Apply throttle for POST requests
    if request.method == 'POST':
        throttle = EmailVerificationThrottle()
        if not throttle.allow_request(request, None):
            from rest_framework.exceptions import Throttled
            raise Throttled(detail="Too many verification attempts. Please try again later.")
    
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
        
        # If GET request (frontend), render success page
        if request.method == 'GET':
            from django.shortcuts import render
            return render(request, 'auth/email_verified.html', {
                'success': True,
                'user': verification.user
            })
        
        # If POST request (API), return JSON
        return Response({'message': 'Email verified successfully'})
    except EmailVerification.DoesNotExist:
        # If GET request (frontend), render error page
        if request.method == 'GET':
            from django.shortcuts import render
            return render(request, 'auth/email_verified.html', {
                'success': False,
                'error': 'Invalid or expired token'
            })
        
        # If POST request (API), return JSON error
        return Response({'error': 'Invalid or expired token'}, 
                       status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def password_reset_request(request):
    """Request password reset - Send email with reset link"""
    # Apply throttle
    throttle = PasswordResetThrottle()
    if not throttle.allow_request(request, None):
        from rest_framework.exceptions import Throttled
        raise Throttled(detail="Too many password reset requests. Please try again later.")
    
    serializer = PasswordResetRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    
    try:
        user = User.objects.get(email=email, is_active=True)
        # Create password reset token
        token = secrets.token_urlsafe(32)
        PasswordResetToken.objects.create(
            user=user,
            token=token,
            expires_at=timezone.now() + timedelta(hours=24)
        )
        
        # Send password reset email
        send_password_reset_email(user, token)
        
        # Always return success message (don't reveal if email exists)
        return Response({
            'message': 'If an account with that email exists, a password reset link has been sent.'
        })
    except User.DoesNotExist:
        # Don't reveal if email exists or not
        return Response({
            'message': 'If an account with that email exists, a password reset link has been sent.'
        })


@api_view(['GET', 'POST'])
@permission_classes([permissions.AllowAny])
def password_reset_confirm(request, token):
    """Password Reset Confirm - Supports both GET (frontend) and POST (API)"""
    if request.method == 'GET':
        # Render password reset form
        from django.shortcuts import render
        try:
            reset_token = PasswordResetToken.objects.get(
                token=token,
                is_used=False,
                expires_at__gt=timezone.now()
            )
            return render(request, 'auth/password_reset_confirm.html', {
                'token': token,
                'valid': True
            })
        except PasswordResetToken.DoesNotExist:
            return render(request, 'auth/password_reset_confirm.html', {
                'token': token,
                'valid': False,
                'error': 'Invalid or expired token'
            })
    
    # POST request - Process password reset
    serializer = PasswordResetConfirmSerializer(data={
        'token': token,
        'password': request.data.get('password'),
        'password_confirm': request.data.get('password_confirm')
    })
    serializer.is_valid(raise_exception=True)
    
    try:
        reset_token = PasswordResetToken.objects.get(
            token=token,
            is_used=False,
            expires_at__gt=timezone.now()
        )
        
        # Set new password
        user = reset_token.user
        user.set_password(serializer.validated_data['password'])
        user.save()
        
        # Mark token as used
        reset_token.is_used = True
        reset_token.save()
        
        # Render success page for frontend
        from django.shortcuts import render
        return render(request, 'auth/password_reset_success.html', {
            'success': True
        })
    except PasswordResetToken.DoesNotExist:
        return Response({'error': 'Invalid or expired token'}, 
                       status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','POST'])
@permission_classes([permissions.IsAuthenticated])
def password_change(request):
    """Change password for logged-in user"""
    serializer = ChangePasswordSerializer(
        data=request.data,
        context={'request': request}
    )
    serializer.is_valid(raise_exception=True)

    user = request.user
    new_password = serializer.validated_data['new_password']

    # Set mật khẩu mới
    user.set_password(new_password)
    user.save()

    # (tuỳ bạn) Xoá token cũ để buộc login lại nếu dùng TokenAuth
    try:
        Token.objects.filter(user=user).delete()
    except:
        pass

    return Response(
        {'message': 'Đổi mật khẩu thành công.'},
        status=status.HTTP_200_OK
    )