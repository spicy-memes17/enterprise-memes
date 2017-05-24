from django.conf.urls import url

from . import views

app_name = 'spicy_memes'
urlpatterns = [
    url(r'^$', views.content, name='content')
]