from django import forms
# from .models import User
from django.core.exceptions import ObjectDoesNotExist

from .models import Post, MyUser, Comment, LikesComment, LikesPost, Tag, MemeGroup
from django.forms import ModelForm, Textarea, Select
from .authenticate import MyBackend
from django.contrib.auth.forms import UserChangeForm



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
            'passwordConfirm': forms.PasswordInput(),
        }

    def clean(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        passwordConfirm = self.cleaned_data.get('passwordConfirm')
        if len(username) < 4:
            raise forms.ValidationError("Username must have at least four characters.")
        if password != passwordConfirm:
            raise forms.ValidationError("Passwords do not match!")
        if len(password) < 8:
           raise forms.ValidationError("Password has to contain at least 8 characters!")
        if password.isdigit():
           raise forms.ValidationError("You password cannot be entirely numeric.")
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
        label='Select a file',
        help_text='max. 5 megabytes')


# data upload mit ModelForm. ist empfohlen, wenn man mit models.py arbeitet
class UploadForm(ModelForm):
    tags = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '1', 'placeholder': 'Enter Spicy Tags'}))
    group = forms.ModelChoiceField(required=False, label='group', queryset=MemeGroup.objects.all())
    
    def __init__(self, user, **kwargs):
        self.user = user
        # self.group = kwargs.pop('group', None)
        super(UploadForm, self).__init__(**kwargs)
        self.fields['group'].queryset = self.user.memegroup_set.all()
        
        

    #fetches tags by name and writes them into a list. if the tag does not exist it is created
    def handle_tags(self, tagstring):
        tag_list = []
        tag = Tag()
        tag_name_list= tagstring.split(',')
        stripped_tag_names= map(lambda x: x.strip(), tag_name_list)
        for tag_name in stripped_tag_names: # not none check?
            if tag_name is not "": # can this happen?
                try:
                    tag= Tag.objects.get(name=tag_name)
                except Tag.DoesNotExist:
                    tag= Tag(name=tag_name)
                    tag.save()
                tag_list.append(tag)
        return tag_list

    def save(self, commit=True):
        obj = super(UploadForm, self).save(commit=False)
        obj.user = self.user
        group = self.cleaned_data.get('group')

        if group is None:
            try:
                group = MemeGroup.objects.get(name='all')
            except ObjectDoesNotExist:  # as this is done exactly once and only on the first post, there surely is a better solution to this. leave it like this if you want it to work
                group = MemeGroup(name='all')
                group.save()

        obj.group = group
        #get list of tags
        tag_names= self.cleaned_data.get('tags')
        tag_list= self.handle_tags(tag_names)                   # self to call functions from same class

        # object has to have a value for id before a relationship can be set

        if commit:
            obj.save()

        #add all tags to the many to many relationship
        if tag_list is not None:
            for tag in tag_list:
                obj.tags.add(tag)
          
        return obj

    class Meta:
        model = Post
        exclude = ('tags',) #don't remove the ,
        fields = ['title', 'description', 'image_field', 'group', 'video_url']
        widgets = {
            'title': Textarea(attrs={'class': 'form-control', 'rows': '1', 'placeholder': 'Spicy Title'}),
            'description': Textarea(
                attrs={'class': 'form-control', 'rows': '5', 'placeholder': 'Enter spicy description'}),
            'video_url': Textarea(attrs={'class': 'form-control', 'rows': '1', 'placeholder': 'URL that allows embedding (e.g. from YouTube)'}),
        }


class SearchForm(forms.Form):
    search_term = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '1' ,'placeholder': 'Enter Spicy Tags'}))

    #has to be false to be able to pass empty boxes
    by_name= forms.BooleanField(required=False)
    by_tag= forms.BooleanField(required=False)

#used for the search performed after clicking on a tag
class TagSearchForm(forms.Form):
    tag = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '1' ,'placeholder': 'Enter Spicy Tags'}))

# data edit with modelform. image field soll nicht editiert werden. Wenn Bild unerwünscht ist, dann lieber löschen
class EditForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description']
        widgets = {
            'title': Textarea(attrs={'class': 'form-control', 'rows': '1', 'placeholder': 'Spicy Title'}),
            'description': Textarea(
                attrs={'class': 'form-control', 'rows': '5', 'placeholder': 'Enter spicy description'}),
        }

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('content', )
        widgets = {
            'content' : Textarea(attrs={'class': 'form-control', 'rows': '5', 'placeholder': 'Share your spicy thoughts.', 'style': 'margin-bottom: 10px'}),
        }
        
class VoteCommentForm(forms.ModelForm):

    class Meta:
        model = LikesComment
        fields = ('likes', )
        
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

# Similar to Django's UserChangeForm but without password field
class EditProfileForm(UserChangeForm):
    class Meta:
        model = MyUser
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        del self.fields['password'] #delete password field
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')


class ChangeProfilePic(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['profile_pic']

        
class LikeForm(forms.ModelForm):

    class Meta:
        model = LikesPost
        fields = ('likes', )


class GroupForm(forms.Form):
    name= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '1' ,'placeholder': 'Enter Spicy Group Name'}))
    #Textarea(attrs={'class': 'form-control', 'rows': '1', 'placeholder': 'Enter a spicy name', 'style': 'margin-bottom: 5px'})

class InviteForm(forms.Form):
    group = forms.ModelChoiceField(required=True, label='Choose a spicy group', queryset=MemeGroup.objects.all())

    def __init__(self, *args, inviter, invitee, **kwargs):
        super(InviteForm, self).__init__(*args, **kwargs)
        self.fields['group'].queryset = inviter.memegroup_set.all().difference(invitee.memegroup_set.all())

    
