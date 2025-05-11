from django.db                  import models
from django.utils.translation   import gettext_lazy as _
from .profile                   import Profile

class BlockedFriend(models.Model):
    blocker = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='blocked')
    blocked_friend = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='blocker')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('blocker', 'blocked_friend'),)
    def __str__(self):
        return f"{self.blocker.username} blocked {self.blocked_friend.username}"
