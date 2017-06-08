from django import forms
# from .models import User
from .models import Post, MyUser, Tag
from django.forms import ModelForm, Textarea
from .authenticate import MyBackend

class SignUpForm(forms.ModelForm):
    passwordConfirm = forms.CharField(widget=forms.PasswordInput(), required=True, label="Confirm password")
    class Meta:
        model = MyUser
        username = forms.CharField(max_length=255, required=True)
        email = forms.CharField(max_length=255, required=True)
        password = forms.CharField(widget=forms.PasswordInput(), required=True)

        fields = ('username', 'email', 'password', 'passwordConfirm')
        widgets = {
            'password': forms.PasswordInput(),
            'passwordConfirm' : forms.PasswordInput(),
        }

    def clean(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        passwordConfirm = self.cleaned_data.get('passwordConfirm')
        if len(username) < 4 or len(password) < 4:
            raise forms.ValidationError("Username and password must have at least four characters.")
        if password != passwordConfirm:
            raise forms.ValidationError("Passwords do not match!")
        if len(list(filter(lambda x: x.username == username, MyUser.objects.all()))) != 0:
            raise forms.ValidationError("Username is already taken!")
        return self.cleaned_data

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
    tags = forms.CharField(required=False, widget=forms.Textarea(
                                                attrs={'class': 'form-control', 'rows': '1', 'placeholder': 'Enter Spicy Tags'}))
    
    def __init__(self, **kwargs):
        self.user = kwargs.pop('user', None)
        #self.group = kwargs.pop('group', None)
        super(UploadForm, self).__init__(**kwargs)

    def save(self, commit=True):
        obj = super(UploadForm, self).save(commit=False)
        obj.user = self.user
        #obj.group = self.group


        #check for errors here first
        tag_list = self.cleaned_data.get('tags', None)
        
        if tag_list is not None:
            for tag_name in tag_list.split(","):
                tag = Tag.objects.get(name=tag_name)
                obj.tags.add(tag)
        
        if commit:
            obj.save()
        return obj
    
    class Meta:
        model = Post
        exclude = ('tags',) #don't remove the ,
        fields = ['title', 'description', 'image_field', 'tags']
        widgets = {
            'title' : Textarea(attrs={'class': 'form-control', 'rows': '1', 'placeholder': 'Spicy Title'}),
            'description' : Textarea(attrs={'class': 'form-control', 'rows': '5', 'placeholder': 'Enter spicy description'}),
            'tags' : Textarea(attrs={'class': 'form-control', 'rows': '1', 'placeholder': 'Enter Spicy Tags'})
        }

        	      #check for errors here first
    def clean_tags_list(self):            #https://stackoverflow.com/questions/5608576/django-enter-a-list-of-values-form-error-when-rendering-a-manytomanyfield-as-a
        data = self.cleaned_data
        tag_list = data.get('tags', None)
        if tag_list is not None:
            for tag_name in actors_list.split(','):
                try:
                    actor = Tag.objects.get(name=tag_name)
                except Tag.DoesNotExist:
                    if FAIL_ON_NOT_EXIST: # decide if you want this behaviour or to create it
                        raise forms.ValidationError('Tag %s does not exist' % tag_name)
                    else: # create it if it doesnt exist
                    Tag(name=tag_name).save()
        return tag_list

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
        username = forms.CharField(max_length=255, required=True)
        password = forms.CharField(widget=forms.PasswordInput(), required=True)
        fields = ('username', 'password')
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        mb = MyBackend()
        user = mb.authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError("Wrong combination for username and password!")
        return self.cleaned_data
        
