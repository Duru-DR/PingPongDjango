from django.db                  import models
from django.utils.translation   import gettext_lazy as _
from .profile                   import Profile

class Friend(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='my_friend')
    friend = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friend_of')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('profile', 'friend'),)
    def __str__(self):
        return f"{self.profile.username} is friend with {self.friend.username}"
