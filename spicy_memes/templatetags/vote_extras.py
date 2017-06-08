from django import template
from ..models import Comment, LikesComment

register = template.Library()

@register.simple_tag
def getVotes(comment):
    return LikesComment.objects.filter(comment=comment).filter(likes=True).count() - LikesComment.objects.filter(comment=comment).filter(likes=False).count()
