from django.conf.urls import url

from . import views

app_name = 'spicy_memes'
urlpatterns = [
    url(r'^$', views.content, name='content'),
    url(r'signUp/', views.signUp, name='signUp'),
    url(r'^userprofile', views.userprofile, name='userprofile'),
    url(r'^trendingPage', views.trendingPage, name='trendingPage'),
    url(r'^freshPage', views.freshPage, name='freshPage'),
    ]