from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'role')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'role', 'is_active', 'is_staff', 'is_superuser')