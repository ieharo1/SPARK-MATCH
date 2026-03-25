from django.db import models
from django.contrib.auth.models import User


class Like(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes_sent')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes_received')
    liked = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'

    def __str__(self):
        action = '❤️ le dio like' if self.liked else '✖️ pasó'
        return f"{self.from_user.username} {action} a {self.to_user.username}"


class Match(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matches_as_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matches_as_user2')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')
        verbose_name = 'Match'
        verbose_name_plural = 'Matches'

    def get_other_user(self, user):
        return self.user2 if self.user1 == user else self.user1

    def get_last_message(self):
        return self.messages.order_by('-created_at').first()

    def unread_count(self, user):
        return self.messages.filter(read=False).exclude(sender=user).count()

    def __str__(self):
        return f"💑 {self.user1.username} & {self.user2.username}"


class Message(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Mensaje'
        verbose_name_plural = 'Mensajes'

    def __str__(self):
        return f"{self.sender.username}: {self.content[:40]}"
