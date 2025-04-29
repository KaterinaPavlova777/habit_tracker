from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    tg_chat_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='tg chat id')

    def __str__(self):
        return self.username
