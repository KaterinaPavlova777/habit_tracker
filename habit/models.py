
from django.db import models

from users.models import User


class Habit(models.Model):
    FREQUENCY = {
        ('day', 'Every day'),
        ('3 days', 'Every 3 days'),
        ('week', 'Every week'),
    }

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habit',
                             verbose_name='user', blank=True, null=True)
    place = models.CharField(max_length=255, verbose_name='place')
    time = models.TimeField(verbose_name='time')
    reward = models.CharField(max_length=255, verbose_name='reward', blank=True, null=True)
    lead_time = models.DurationField(verbose_name='lead time')
    is_public = models.BooleanField(default=False, verbose_name='public')
    action = models.CharField(max_length=255, verbose_name='action')
    pleasant = models.BooleanField(verbose_name='pleasant')
    related = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True,
                                related_name='related_habit', verbose_name='related')
    periodicity = models.CharField(max_length=30, choices=FREQUENCY, default='day',
                                   verbose_name='periodicity')

    def __str__(self):
        return f"{self.pk} : {self.user}"
