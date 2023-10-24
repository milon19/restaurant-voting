from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='menus', on_delete=models.CASCADE)
    date = models.DateField()

    '''
    Creating item field as CharField for now to make it simple. It will store comma (,) separated item.
    ex: Mutton,Chicken,Fish
    '''
    item = models.CharField(max_length=255)
