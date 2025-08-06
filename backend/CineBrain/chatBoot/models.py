from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.

class Room(models.Model):
    title = models.CharField(max_length=254)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class Message(models.Model):
    SENDERS = [
        ('user', 'user'),
        ('model', 'model'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    sender = models.CharField(max_length=5, choices=SENDERS, default='user')
    message = models.TextField( default='')
