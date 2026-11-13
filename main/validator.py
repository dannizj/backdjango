from django import forms
from django.core.exceptions import ValidationError
from main.models import User

class UserValidatorForm(forms.Form):
    name = forms.CharField(max_length=100, min_length=3, required=True)
    surname = forms.CharField(max_length=100, min_length=2, required=True)
    nick = forms.CharField(max_length=70, min_length=3, required=True)
    email = forms.EmailField(required=True)
    bio = forms.CharField(required=False)
    password = forms.CharField(required=True)