from django.conf.urls import url

from . import views

app_name = 'spicy_memes'
urlpatterns = [
    url(r'^$', views.content, name='content'),
    url(r'^(?P<content>((fresh)|(spicy)|(on_fire)))/$', views.content, name='content'),
    url(r'^post/(?P<pk>\d+)/detail/$', views.postDetail, name='postDetail'),
    url(r'^post/(?P<pk>\d+)/editPost/$', views.editPost, name='editPost'),
    url(r'signUp/', views.signUp, name='signUp'),
    url(r'logOut/', views.logOut, name='logOut'),
    url(r'^userprofile/(?P<user_name>\w+)/$', views.userprofile, name='userprofile'),
    url(r'^userprofile/(?P<user_name>\w+)/edit_profile', views.edit_profile, name='edit_profile'),
    url(r'^loginPage', views.loginPage, name='loginPage'),
    url(r'^uploadFile', views.uploadFile, name='uploadFile'),
    url(r'^post/(?P<pk>\d+)/delete/$', views.deleteFile, name='deleteFile'),
    url(r'^logout', views.logOut, name='logoutPage'),
    url(r'^userprofile/(?P<user_name>\w+)/deleteUser', views.deleteUser, name='deleteUser'),
    url(r'^search', views.search, name='search'),
  #  url(r'^edit_profile/(?P<user_name>\w+)/$', views.edit_profile, name='edit_profile'),
    url(r'^userprofile/(?P<user_name>\w+)/change_password', views.change_password, name='change_password'),
    url(r'^userprofile/(?P<user_name>\w+)/changeProfilePic', views.changeProfilePic, name='changeProfilePic'),
    url(r'^post/(?P<pk>\d+)/(?P<likes>(\d+))/likePost/$', views.likePost, name='likePost'),
    url(r'^post/(?P<pk>\d+)/comment/$', views.addComment, name='addComment'),
    url(r'^post/(?P<pk>\d+)/comment/delete/$', views.deleteComment, name='deleteComment'),
    url(r'^post/(?P<pk>(\d+))/(?P<likes>(\d+))/vote/$', views.voteComment, name='voteComment'),
    url(r'^startPage/', views.startPage, name='startPage'),
    ]
