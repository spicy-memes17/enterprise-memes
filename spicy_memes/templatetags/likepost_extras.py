from django import template
from ..models import Post, LikesPost

register = template.Library()


@register.simple_tag
def getPostLikes(post):
    return LikesPost.objects.filter(post=post).filter(likes=True).count() - LikesPost.objects.filter(
        post=post).filter(likes=False).count()

@register.simple_tag
def getnegPostLikes(post):
    return LikesPost.objects.filter(post=post).filter(likes=True).count() - LikesPost.objects.filter(
        post=post).filter(likes=False).count() * -1

@register.simple_tag
def positivlikes(post):
    ret =True
    if getPostLikes(post) < 0:
        ret = False
    return ret
@register.filter
def hasUpVotedPost(user, post):
    if (LikesPost.objects.filter(post=post).filter(user=user).filter(likes=True)):
        return True
    else:
        return False

@register.filter
def isVideo(post):
    if "http" in post.video_url:
        return True
    else:
        return False

@register.filter
def hasDownVotedPost(user, post):
    if (LikesPost.objects.filter(post=post).filter(user=user).filter(likes=False)):
        return True
    else:
        return False


@register.filter
def isPostAuthor(user, post):
    if (post.user == user):
        return True
    else:
        return False
