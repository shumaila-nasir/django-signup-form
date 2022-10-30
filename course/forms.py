from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django import forms


class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email' , 'password1', 'password2']

class EditForm(UserChangeForm):
    password = None
    class Meta:
        model= User
        fields = ['username', 'first_name', 'last_name', 'email', 'date_joined', 'last_login']


class EditAdminForm(UserChangeForm):
    password = None
    class Meta:
        model= User
        fields = '__all__'