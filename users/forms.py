from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']
