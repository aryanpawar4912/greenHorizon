# profile_tags.py
from django import template
from myapp.models import Profile

register = template.Library()

@register.simple_tag(takes_context=True)
def get_user_profile(context):
    user = context['request'].user
    if user.is_authenticated:
        try:
            return Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            return None
    return None