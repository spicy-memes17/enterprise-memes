from django import forms
from .models import MyUser

class SignUpForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ('username', 'email', 'password')
    # username = forms.CharField(label = 'Username')
    # email = forms.EmailField(label = 'Email')
    # password = forms.CharField(label = 'Password', widget=forms.PasswordInput)

