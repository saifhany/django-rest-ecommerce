# tasks.py
from celery import shared_task
from django.core.mail import send_mail
@shared_task
def send_welcome_email(email, username, verify_url=None):
    subject = 'Welcome!'
    message = f'Hello {username}.\nWelcome.\nVerify: {verify_url}' if verify_url else f'Hello {username}.'
    send_mail(subject, message, 'no-reply@example.com', [email])
    return True
