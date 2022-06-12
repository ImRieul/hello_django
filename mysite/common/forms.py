from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserForm(UserCreationForm):
    email = forms.EmailField(label='Email')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')
        # password1 : 비밀번호
        # password2 : 비밀번호 대조용