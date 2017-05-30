from django.conf.urls import url

from . import views

app_name = 'spicy_memes'
urlpatterns = [
    url(r'^$', views.content, name='content'),
    url(r'signUp/', views.signUp, name='signUp'),
    url(r'logOut/', views.logOut, name='logOut'),
    url(r'^userprofile', views.userprofile, name='userprofile'),
    url(r'^trendingPage', views.trendingPage, name='trendingPage'),
    url(r'^freshPage', views.freshPage, name='freshPage'),
    url(r'^loginPage', views.loginPage, name='loginPage'),
    url(r'^logout', views.logOut, name='logoutPage'),
    url(r'^deleteUser', views.deleteUser, name='deleteUser')
    ]