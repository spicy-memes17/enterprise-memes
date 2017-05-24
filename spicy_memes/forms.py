from django import forms
# from .models import User

class SignUp(forms.Form):
    username = forms.CharField(label = 'Username')
    email = forms.EmailField(label = 'Email')
    password = forms.CharField(label = 'Password', widget=forms.PasswordInput)

