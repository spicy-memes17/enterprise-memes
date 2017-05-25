from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Statistic)
admin.site.register(MemeGroup)
admin.site.register(MyUser)
