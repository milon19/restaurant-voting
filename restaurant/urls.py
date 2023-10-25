from django.urls import path

from restaurant.views import RestaurantViewSet, MenuViewSet

app_name = "restaurant"

urlpatterns = [
    path("create/", RestaurantViewSet.as_view({'post': 'create'}), name="create_restaurant"),
    path("list/", RestaurantViewSet.as_view({'get': 'list'}), name="restaurant_list"),
    path("menu/create/", MenuViewSet.as_view({'post': 'create'}), name="create_menu"),
    path("menu/today/", MenuViewSet.as_view({'get': 'list'}), name="menu_list"),
]

