from .models import MyUser

class MyBackend(object):
    def authenticate(self, request, username=None, password=None):
        users = MyUser.objects.all() #get all users
        user = list(filter(lambda x: x.username == username, users)) # look for desired user -> there is probably a more elegant way to do this
        if len(user) == 0: # no such user in database
        	return None
        else:
        	user = user[0]
        	if user.password == password:
        		return user
        	else:
        		return None

    def get_user(self, user_id):
        try:
            return MyUser.objects.get(pk=user_id)
        except MyUser.DoesNotExist:
            return None