"""
Utility functions for user management
"""
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse


def send_verification_email(user, token):
    """
    Send email verification email to user
    
    Args:
        user: User instance
        token: Verification token string
    """
    verification_url = settings.BASE_URL + reverse('users:verify_email', kwargs={'token': token})
    
    context = {
        'user': user,
        'verification_url': verification_url,
        'site_name': 'BookReview.vn',
    }
    
    # Render email templates
    subject = f'Xác nhận email đăng ký - {context["site_name"]}'
    html_message = render_to_string('emails/verification_email.html', context)
    plain_message = render_to_string('emails/verification_email.txt', context)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        # Log error in production
        print(f"Error sending verification email: {e}")
        return False


def send_password_reset_email(user, token):
    """
    Send password reset email to user
    
    Args:
        user: User instance
        token: Password reset token string
    """
    reset_url = settings.BASE_URL + reverse('users:password_reset_confirm', kwargs={'token': token})
    
    context = {
        'user': user,
        'reset_url': reset_url,
        'site_name': 'BookReview.vn',
    }
    
    # Render email templates
    subject = f'Đặt lại mật khẩu - {context["site_name"]}'
    html_message = render_to_string('emails/password_reset_email.html', context)
    plain_message = render_to_string('emails/password_reset_email.txt', context)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        # Log error in production
        print(f"Error sending password reset email: {e}")
        return False

