from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class ChatRoom(models.Model):
    name = models.CharField(max_length=128)
    users_online = models.ManyToManyField(User, blank=True, related_name="online_users")

    def __str__(self):
        return self.name


class ChatMessage(models.Model):
    room = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE, related_name="chat_message"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        ordering = ["-created"]
