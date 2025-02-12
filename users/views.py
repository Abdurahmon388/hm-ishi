from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, VerifyEmailSerializer, LoginSerializer, UserSerializer
from rest_framework import generics, status
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()

class RegisterView(generics.CreateAPIView):
    """
    Foydalanuvchini ro‘yxatdan o‘tkazish.
    """
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        send_mail(
            'Tasdiqlash Kodingiz',
            f'Sizning tasdiqlash kodingiz: {user.verification_code}',
            'admin@example.com',
            [user.email],
            fail_silently=False,
        )


class VerifyEmailView(generics.GenericAPIView):
    """
    Email tasdiqlash (kod orqali).
    """
    serializer_class = VerifyEmailSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response({"detail": "Email muvaffaqiyatli tasdiqlandi!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    """
    Foydalanuvchini tizimga kiritish.
    """
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """
    Authenticated foydalanuvchi profilini olish.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class LogoutView(APIView):
    """
    Tizimdan chiqish (JWT tokendan foydalanib).
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Tizimdan muvaffaqiyatli chiqildi!"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Noto'g'ri yoki eskirgan token!"}, status=status.HTTP_400_BAD_REQUEST)


class UserIPView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ip = request.META.get('HTTP_X_FORWARDED_FOR')
        if ip:
            ip = ip.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        return Response({"ip_address": ip})
