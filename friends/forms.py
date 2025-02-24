from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter your username',
        'class': 'form-control',
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Enter your email address',
        'class': 'form-control',
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter your password',
        'class': 'form-control',
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm your password',
        'class': 'form-control',
    }))

class LogInForm(AuthenticationForm):
    username = UsernameField(label='Enter username', widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    password = forms.CharField(label='Enter password', widget=forms.PasswordInput(attrs={
        'class':'form-control',
    }))
