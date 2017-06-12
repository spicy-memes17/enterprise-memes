from django import template
from ..models import Post, LikesPost

register = template.Library()


@register.simple_tag
def getLikes(post):
    return LikesPost.objects.filter(post=post).filter(likes=True).count() - LikesPost.objects.filter(
        post=post).filter(likes=False).count()


@register.filter
def hasUpVoted(user, post):
    if (LikesPost.objects.filter(post=post).filter(user=user).filter(likes=True)):
        return True
    else:
        return False


@register.filter
def hasDownVoted(user, post):
    if (LikesPost.objects.filter(post=post).filter(user=user).filter(likes=False)):
        return True
    else:
        return False


@register.filter
def isAuthor(user, post):
    if (post.user == user):
        return True
    else:
        return False