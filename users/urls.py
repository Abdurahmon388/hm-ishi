from django.urls import path
from .views import UserProfileView, RegisterView, VerifyEmailView, LoginView


urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('register/', RegisterView.as_view(), name='register'),
    path('verify/email/', VerifyEmailView.as_view(), name='verify_email'),
    path('login/', LoginView.as_view(), name='login'),
]
