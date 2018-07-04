__author__ = 'yangjian'
__date__ = '2018/6/29 15:56'

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254,required=True,widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ('username','email','password1','password2')