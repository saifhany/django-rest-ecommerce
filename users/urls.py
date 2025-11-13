from django.urls import path
from .views import RegisterView, VerifyEmailView, ForgotPasswordView, ResetPasswordView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', TokenObtainPairView.as_view()),
    path('refresh', TokenRefreshView.as_view()),
    path('verify-email', VerifyEmailView.as_view()),
    path('forgot-password', ForgotPasswordView.as_view()),
    path('reset-password/', ResetPasswordView.as_view()),
]
