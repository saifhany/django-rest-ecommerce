from rest_framework import generics, status
from .serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
import os
frontend_url = os.getenv("DJANGO_FRONTEND_URL", "http://localhost:8000")

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class VerifyEmailView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = AccessToken(token)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
                return Response({'message':'Email verified'}, status=status.HTTP_200_OK)
            return Response({'message':'Already verified'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'error':'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        if not user:
            return Response({'error':'User not found'}, status=404)
        token = PasswordResetTokenGenerator().make_token(user)
        reset_url = f"{frontend_url}/api/auth/reset-password/?uid={user.id}&token={token}"
        send_mail('Reset password', f'Use this link to reset: {reset_url}', 'no-reply@example.com', [email])
        return Response({'message':'Password reset email sent'})

class ResetPasswordView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        uid = request.GET.get('uid')
        token = request.GET.get('token')
        password = request.data.get('password')
        try:
            user = User.objects.get(id=uid)
        except User.DoesNotExist:
            return Response({'error':'Invalid user'}, status=400)
        gen = PasswordResetTokenGenerator()
        if not gen.check_token(user, token):
            return Response({'error':'Invalid or expired token'}, status=400)
        user.set_password(password)
        user.save()
        return Response({'message':'Password reset successful'})
