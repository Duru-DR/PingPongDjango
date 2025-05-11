from django.db      import models
from prfl.models    import Profile

class Chat(models.Model):
    user1 = models.ForeignKey(Profile, related_name='user1_chats', on_delete=models.CASCADE)
    user2 = models.ForeignKey(Profile, related_name='user2_chats', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, unique=True)
    last_message_time = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = (('user1', 'user2'),)
    
    def __str__(self):
        return f'Chat between {self.user1} and {self.user2}'
