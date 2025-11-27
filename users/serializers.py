from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.contenttypes.models import ContentType
from .models import User, Profile
from shelves.models import Shelf
from social.models import Follow
from .validators import validate_password_strength


class ProfileSerializer(serializers.ModelSerializer):
    """Profile Serializer"""
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    role = serializers.CharField(source='user.role', read_only=True)
    
    following_count = serializers.SerializerMethodField() # List of users this user is following
    follower_count = serializers.SerializerMethodField() # Fan count for Reviewers
    
    is_fully_completed = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            'username', 'email', 'role', 'avatar', 'bio', 'location', 'website',
            'facebook_url', 'twitter_url', 'instagram_url', 'language',
            'notify_follow', 'notify_review_like', 'notify_comment', 
            'notify_mention',
            'following_count', 'follower_count', 'is_fully_completed'
        ]
        read_only_fields = ['username', 'email', 'role']

    def get_following_count(self, obj):
        return obj.user.following.count()

    def get_follower_count(self, obj):
        # Chỉ Reviewer mới hiện số Fan
        if obj.user.role == User.Role.REVIEWER:
            user = obj.user
            user_content_type = ContentType.objects.get_for_model(User)
            
            return Follow.objects.filter(
                content_type=user_content_type, 
                object_id=user.id
            ).count()
        
        return 0

    def get_is_fully_completed(self, obj):
        user = obj.user
        
        has_bio = bool(obj.bio and obj.bio.strip())
        
        has_email = bool(user.email and user.email.strip())
        has_name = bool(user.first_name and user.last_name)
        
        return has_bio and has_email and has_name


class UserSerializer(serializers.ModelSerializer):
    """User Serializer"""
    profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                  'role', 'is_verified', 'date_joined', 'profile']
        read_only_fields = ['id','role', 'is_verified', 'date_joined']

    def get_profile(self, obj):
        if hasattr(obj, 'profile'):
            return ProfileSerializer(obj.profile).data
        return None



class RegisterSerializer(serializers.ModelSerializer):
    """Registration Serializer"""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password, validate_password_strength])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        
        # 1. Tạo User: Luôn ép role là READER, is_staff=False
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=User.Role.READER, # Quan trọng: Ép cứng role
            is_active=True # Hoặc False nếu bạn muốn bắt xác thực email trước
        )

        # 2. Tạo Profile trống đi kèm
        Profile.objects.create(user=user)

        # 3. Tạo 3 Kệ sách mặc định (System Shelves)
        # WTR: Want to Read, READING: Reading, READ: Read
        default_shelves = [
            {'name': 'Want to Read', 'system_type': 'WTR'},
            {'name': 'Currently Reading', 'system_type': 'READING'},
            {'name': 'Read', 'system_type': 'READ'},
        ]
        
        for shelf_data in default_shelves:
            Shelf.objects.create(
                user=user,
                name=shelf_data['name'],
                system_type=shelf_data['system_type'],
                visibility='public'
            )

        return user
class LoginSerializer(serializers.Serializer):
    """Login Serializer"""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                              username=username, password=password)
            if not user:
                raise serializers.ValidationError('Invalid username or password.')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Must include "username" and "password".')
        return attrs


class PasswordResetRequestSerializer(serializers.Serializer):
    """Password Reset Request Serializer"""
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        try:
            User.objects.get(email=value, is_active=True)
        except User.DoesNotExist:
            # Don't reveal if email exists or not for security
            pass
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Password Reset Confirm Serializer"""
    token = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password, validate_password_strength])
    password_confirm = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password_confirm = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Mật khẩu hiện tại không đúng.")
        return value

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        new_password_confirm = attrs.get('new_password_confirm')

        if new_password != new_password_confirm:
            raise serializers.ValidationError({
                "new_password_confirm": "Mật khẩu nhập lại không khớp."
            })

        # Dùng validator của Django để check độ mạnh mật khẩu
        user = self.context['request'].user
        validate_password(new_password, user)

        return attrs