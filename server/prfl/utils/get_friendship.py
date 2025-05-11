from django.db.models   import Q
from ..models           import Friend

def get_friendship(profile1, profile2):
    if profile1 == profile2:
        return None

    friendship = Friend.objects.filter(
        (Q(profile=profile1) & Q(friend=profile2)) |
        (Q(profile=profile2) & Q(friend=profile1))
    ).first()

    return friendship
