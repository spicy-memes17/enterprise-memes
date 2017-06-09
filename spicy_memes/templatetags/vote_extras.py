from django import template
from ..models import Comment, LikesComment

register = template.Library()

@register.simple_tag
def getVotes(comment):
    return LikesComment.objects.filter(comment=comment).filter(likes=True).count() - LikesComment.objects.filter(comment=comment).filter(likes=False).count()

@register.filter
def hasUpVoted(user, comment):
    if(LikesComment.objects.filter(comment=comment).filter(user=user).filter(likes=True)):
        return True
    else:
        return False

@register.filter
def hasDownVoted(user, comment):
    if(LikesComment.objects.filter(comment=comment).filter(user=user).filter(likes=False)):
        return True
    else:
        return False
