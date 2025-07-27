from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm

class SignupForm(UserCreationForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'user_type', 'profile_picture',
                  'address_line1', 'city', 'state', 'pincode', 'password1', 'password2']
