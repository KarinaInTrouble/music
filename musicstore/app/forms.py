from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Обязательное поле. Введите действующий адрес электронной почты.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']