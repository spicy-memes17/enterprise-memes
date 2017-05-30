from django import forms
# from .models import User
from .models import Post, MyUser
from django.forms import ModelForm, Textarea

class SignUpForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ('username', 'email', 'password')

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

# data upload mit ModelForm. ist empfohlen, wenn man mit models.py arbeitet
class UploadForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'image_field']
        widgets = {
            'title' : Textarea(attrs={'class': 'form-control', 'rows': '1', 'placeholder': 'Spicy Title'}),
            'description' : Textarea(attrs={'class': 'form-control', 'rows': '5', 'placeholder': 'Enter spicy description'}),
        }

# data edit with modelform. image field soll nicht editiert werden. Wenn Bild unerwünscht ist, dann lieber löschen
class EditForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description']
        widgets = {
            'title' : Textarea(attrs={'class': 'form-control', 'rows': '1', 'placeholder': 'Spicy Title'}),
            'description' : Textarea(attrs={'class': 'form-control', 'rows': '5', 'placeholder': 'Enter spicy description'}),
        }


class LogInForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ('username', 'password')
