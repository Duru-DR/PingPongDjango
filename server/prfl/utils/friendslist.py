from django.db.models           import Q
from ..models                   import Profile, Friend

def friendslist(profile, prefix=None):
    if not prefix:
        friendships = Friend.objects.filter(
            Q(profile=profile) | Q(friend=profile)
        )
    else:
        friendships = Friend.objects.filter(
            Q(profile=profile, friend__username__icontains=prefix) |
            Q(friend=profile, profile__username__icontains=prefix)
        )
    
    friends_data = []
    for friendship in friendships:
        if friendship.profile == profile:
            friend = friendship.friend
        else:
            friend = friendship.profile

        friends_data.append({
            "username": friend.username,
            "is_online": friend.is_online,
            "picture": friend.picture if friend.picture else None,
            "rank": friend.rank,
            "badge": friend.badge
        })
    return friends_data