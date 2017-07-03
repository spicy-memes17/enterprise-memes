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
    url(r'^userprofile', views.userprofile, name='userprofile'),
    url(r'^loginPage', views.loginPage, name='loginPage'),
    url(r'^uploadFile', views.uploadFile, name='uploadFile'),
    url(r'^post/(?P<pk>\d+)/delete/$', views.deleteFile, name='deleteFile'),
    url(r'^logout', views.logOut, name='logoutPage'),
    url(r'^deleteUser', views.deleteUser, name='deleteUser'),
    url(r'^search', views.search, name='search'),
    url(r'^like-post/$', views.like_post, name='like_post'),
    url(r'^like-comment/$', views.like_comment, name='like_comment'),
    url(r'^edit_profile', views.edit_profile, name='edit_profile'),
    url(r'^change_password', views.change_password, name='change_password'),
    url(r'^changeProfilePic', views.changeProfilePic, name='changeProfilePic'),
    url(r'^post/(?P<pk>\d+)/comment/$', views.addComment, name='addComment'),
    url(r'^post/(?P<pk>\d+)/comment/delete/$', views.deleteComment, name='deleteComment'),
    url(r'^startPage/', views.startPage, name='startPage'),
    url(r'^createGroup', views.createGroup, name= 'createGroup'),
    url(r'^leaveGroup/(?P<name_group>.*)/(?P<name_user>.*)', views.leaveGroup, name='leaveGroup'),
    url(r'^acceptInvite/(?P<name_group>.*)/(?P<name_user>.*)', views.acceptInvite, name='acceptInvite'),
    url(r'^declineInvite/(?P<name_group>.*)/(?P<name_user>.*)', views.declineInvite, name='declineInvite'),
    url(r'^groupDetail/(?P<group_name>.*)', views.groupDetail, name='groupDetail')
    ]
