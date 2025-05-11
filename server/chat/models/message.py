from django.db      import models
from .chat          import Chat
from prfl.models    import Profile

class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(Profile, related_name='sender_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(Profile, related_name='receiver_messages', on_delete=models.CASCADE)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Message from {self.sender} to {self.receiver} in chat {self.chat}'
