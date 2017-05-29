from django import forms
# from .models import User
from .models import Post

class SignUp(forms.Form):
    username = forms.CharField(label = 'Username')
    email = forms.EmailField(label = 'Email')
    password = forms.CharField(label = 'Password', widget=forms.PasswordInput)


# data upload
class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=200)	
    description = forms.CharField(max_length=2000,
        widget=forms.Textarea(
            attrs={
                'rows': '5',
                'placeholder': 'Type your spicy description here',
            }))
    image_field = forms.FileField(
        label ='Select a file',
        help_text='max. 5 megabytes')

    
