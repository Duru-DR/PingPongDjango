from django.db                  import models
from django.utils.translation   import gettext_lazy as _
from .profile                   import Profile

class Notification(models.Model):
    NOTIFICATION_TYPE_CHOICES = [
        ('FRIENDSHIP_REQUEST', 'Friendship request'),
        ('HANDLE_REQUESTED_FRIENDSHIP', 'Handle request friendship'),
        ('PLAYWITHME_REQUEST', 'PlayWithMe request'),
        ('JOINING_TOURNAMENT', 'Joining Tournament'),
        ('TOURNAMENT_REMINDER', 'Tournament reminder'),
    ]

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='notifications')
    content = models.TextField()
    from_user = models.CharField(max_length=150)
    created_at = models.DateTimeField(_("created_at"), auto_now_add=True)
    notification_type = models.CharField(
        max_length=50,
        choices=NOTIFICATION_TYPE_CHOICES,
        default='FRIENDSHIP_REQUEST'
    )

    class Meta:
        ordering = ['created_at']
