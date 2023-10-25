from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from restaurant.models import Restaurant, Menu


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'

    def create(self, validated_data):
        restaurant = validated_data['restaurant']
        date = validated_data['date']

        if Menu.objects.filter(restaurant=restaurant, date=date).exists():
            raise ValidationError("A menu for this restaurant on this date already exists.")

        menu = Menu.objects.create(**validated_data)
        return menu
