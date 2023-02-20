from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm, TextInput, Textarea

from .models import *


# class feedbackForm(ModelForm):
#     class Meta:
#         model = Feedback
#         fields = ['title', 'question']
#         widgets = {"title": TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Укажите тему письма'
#         }),
#         'question':  Textarea(attrs={
#             'class': 'form-control',
#             'placeholder': 'Напишите сообщение...'})}


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'name@example.com'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
    'class': 'form-input',
    'placeholder': 'Квартира'}))
#    placeholder=""