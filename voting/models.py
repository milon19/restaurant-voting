from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.utils import timezone

from restaurant.models import Menu, Restaurant

User = get_user_model()


class VotingManager(models.Manager):
    def get_votes_for_today_menus(self):
        today = timezone.now().date()
        return self.filter(menu__date=today)

    def get_restaurants_with_votes_today(self):
        today = timezone.now().date()

        restaurants_with_votes = (
            self.filter(menu__date=today)
            .values('menu__restaurant')
            .annotate(total_votes=Count('id'))
            .order_by('-total_votes')
        )

        restaurant_list = list(
            {
                'restaurant_id': restaurant['menu__restaurant'],
                'total_votes': restaurant['total_votes'],
            }
            for restaurant in restaurants_with_votes
        )

        restaurant_list.sort(key=lambda x: x['total_votes'], reverse=True)

        return restaurant_list


class Voting(models.Model):
    user = models.ForeignKey(User, related_name='votes', on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, related_name='votes', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'menu')

    objects = VotingManager()


class VotingResult(models.Model):
    date = models.DateField()
    winner = models.ForeignKey(Restaurant, related_name='results', on_delete=models.CASCADE)
    total_vote = models.IntegerField(default=0)
