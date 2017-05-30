from django import forms
from .models import MyUser

class SignUpForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ('username', 'email', 'password')

class LogInForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ('username', 'password')
