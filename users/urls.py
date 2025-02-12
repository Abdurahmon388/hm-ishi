from django.urls import path
from .views import RegisterView, VerifyEmailView, LoginView, UserProfileView, LogoutView, UserIPView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify/email/', VerifyEmailView.as_view(), name='verify-email'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('ip/', UserIPView.as_view(), name='user-ip'),
]

