# signals.py
import os
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from .tasks import send_welcome_email
User = get_user_model()
frontend_url = os.getenv("DJANGO_FRONTEND_URL", "http://localhost:8000")



@receiver(post_save, sender=User)
def send_verification_email(sender, instance, created, **kwargs):
    if created and instance.email:
        token = RefreshToken.for_user(instance).access_token
        verify_url = f"{frontend_url}/api/auth/verify-email?token={token}"
        # schedule welcome + verification via celery task (task also prints to console backend)
        send_welcome_email.delay(instance.email, instance.username, verify_url)
