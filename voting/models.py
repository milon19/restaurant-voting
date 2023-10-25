from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from restaurant.models import Menu

User = get_user_model()


class VotingManager(models.Manager):
    def get_votes_for_today_menus(self):
        today = timezone.now().date()
        return self.filter(menu__date=today)


class Voting(models.Model):
    user = models.ForeignKey(User, related_name='votes', on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, related_name='votes', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'menu')

    objects = VotingManager()
