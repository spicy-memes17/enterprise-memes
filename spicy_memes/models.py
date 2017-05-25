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
    date = models.DateTimeField()
    image_field = models.ImageField(upload_to='images/', default='media/images/image.jpg')

    tags = models.ManyToManyField('Tag', blank=True)
    statistic = models.OneToOneField('Statistic', on_delete=models.CASCADE)#cascading -> when passing multiple parameters, the other table's name seems to have to be in ''
    group = models.ForeignKey('Group', on_delete=models.CASCADE)#ForeignKey models a 1 to Many relationship
    user = models.ForeignKey('MyUser', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class MyUser(AbstractBaseUser, PermissionsMixin): #we don't need all attributes of the django user model. extending AbstractBaseUser allows us to create a custom user model
    username = models.CharField(max_length=15, unique=True)
    email = models.EmailField()
    profile_pic = models.ImageField(upload_to='images/', default='media/images/image.jpg')

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


class Group(models.Model): #there is a group model in django. we could use it, but it doesn't seem necessary to me https://docs.djangoproject.com/en/1.11/ref/contrib/auth/#django.contrib.auth.models.Group
    name = models.CharField(max_length=30)
    users = models.ManyToManyField(MyUser)

    def __str__(self):
        return self.name


class Statistic(models.Model):
    upvotes = models.PositiveIntegerField()
    downvotes = models.PositiveIntegerField()

    def __str__(self):
        return self.id


class Comment(models.Model):
    date = models.DateTimeField()
    content = models.CharField(max_length=500)
    statistic = models.OneToOneField(Statistic, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    def __str__(self):
        return self.id


#ADDITIONAL INFO IF SOMETHING GOES WRONG:
    #add this to the settings.py BEFORE MIGRATION
    #AUTH_USER_MODEL = 'spicy_memes.MyUser'


#https://www.caktusgroup.com/blog/2013/08/07/migrating-custom-user-model-django/
