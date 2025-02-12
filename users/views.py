from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, RegisterSerializer, VerifyEmailSerializer, LoginSerializer

from rest_framework import generics, status
from django.core.mail import send_mail
from rest_framework_simplejwt.views import TokenObtainPairView


User = get_user_model()


class RegisterView(generics.CreateAPIView):
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
    serializer_class = VerifyEmailSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response({"detail": "Email muvaffaqiyatli tasdiqlandi!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

#
