from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.utils import timezone

#TODO:
#ensure at least one item in 1..*
#cascading
#min_length does not exist for models. find substitute to enforce a minimum password length


class Tag(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    date = models.DateTimeField(auto_now_add=True)
    image_field = models.ImageField(upload_to='images/', default='media/images/image.jpg', max_length=40)

    tags = models.ManyToManyField('Tag', blank=True)
    #default = 1 for first sprint version of meme upload
    group = models.ForeignKey('MemeGroup', default = 1, on_delete=models.CASCADE)#ForeignKey models a 1 to Many relationship
    user = models.ForeignKey('MyUser', on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ": " + self.description


class MyUser(AbstractBaseUser, PermissionsMixin): #we don't need all attributes of the django user model. extending AbstractBaseUser allows us to create a custom user model
    username = models.CharField(max_length=15, unique=True)
    email = models.EmailField()
    profile_pic = models.FileField(upload_to='images/', default='default_user_pic.jpg')

    #a password field seems to already exist in the AbstractBaseUser. django documentation is shit

    USERNAME_FIELD = 'username' #probably maps custom names to internal names used for user actions
    EMAIL_FIELD = 'email'

    REQUIRED_FIELDS = ['email']# "A list of the field names that will be prompted for when creating a user via the createsuperuser management command"
    #"REQUIRED_FIELDS must contain all required fields on your user model, but should not contain the USERNAME_FIELD or password as these fields will always be prompted for."

    objects =  UserManager() # used to create users the django way, as our model does not have a password field

    #not inherited from abstract user. have to be set
    date_joined = models.DateTimeField('date joined', default=timezone.now)#, default=timezone.now
    is_active   = models.BooleanField(default=True)
    is_admin    = models.BooleanField(default=False)
    is_staff    = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)
    #has_module_perms = models.BooleanField(default=False)

    def get_full_name(self):
        """Return the email."""
        return self.email

    def get_short_name(self):
        """Return the email."""
        return self.email

    def __str__(self):
        return self.username


class MemeGroup(models.Model): #there is a group model in django. we could use it, but it doesn't seem necessary to me https://docs.djangoproject.com/en/1.11/ref/contrib/auth/#django.contrib.auth.models.Group
    name = models.CharField(max_length=30)
    users = models.ManyToManyField(MyUser)

    def __str__(self):
        return self.name


class Comment(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=500)
    user = models.ForeignKey('MyUser', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + ": " + self.content[0:10]


class LikesPost(models.Model):
    class Meta:
        unique_together = (('user','post'),)

    user = models.ForeignKey('MyUser', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    likes = models.BooleanField(default=True)



    def __str__(self):
        return str(self.user) + " likes " if self.likes else " dislikes " + str(self.post)


class LikesComment(models.Model):
    class Meta:
        unique_together = (('user','comment'),)

    user = models.ForeignKey('MyUser', on_delete=models.CASCADE)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE)
    likes = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user) + (" likes " if self.likes else " dislikes ") + str(self.comment)


#ADDITIONAL INFO IF SOMETHING GOES WRONG:
    #add this to the settings.py BEFORE MIGRATION
    #AUTH_USER_MODEL = 'spicy_memes.MyUser'


#https://www.caktusgroup.com/blog/2013/08/07/migrating-custom-user-model-django/
