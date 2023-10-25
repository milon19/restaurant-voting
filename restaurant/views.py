from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from restaurant.serializers import RestaurantSerializer, MenuSerializer
from restaurant.models import Restaurant, Menu


class RestaurantViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()


class MenuViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MenuSerializer
    queryset = Menu.objects.get_todays_menu()
