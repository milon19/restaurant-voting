import logging

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.utils import timezone

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from restaurant.models import Menu, Restaurant

User = get_user_model()


class RestaurantViewSetTestCase(APITestCase):
    login_url = reverse('authentication:login')

    email = 'milon@yopmail.com'
    password = 'milon123'

    def setUp(self):
        logging.getLogger('django').setLevel(logging.ERROR)
        self.user = User.objects.create_user(self.email, self.password)

    def _login(self):
        data = {
            'email': self.email, 'password': self.password
        }
        r = self.client.post(self.login_url, data)
        body = r.json()
        if 'access' in body:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer %s' % body['access'])
        return r.status_code, body

    def test_list_restaurants(self):
        self._login()
        url = reverse("restaurant:restaurant_list")
        Restaurant.objects.create(name='Restaurant A', address='Dhaka')
        Restaurant.objects.create(name='Restaurant B', address='Mirpur')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_restaurant(self):
        self._login()
        url = reverse("restaurant:create_restaurant")
        data = {
            'name': 'New Restaurant',
            'address': 'Dhanmondi'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Restaurant.objects.filter(name='New Restaurant').exists())


class MenuViewSetTestCase(APITestCase):
    login_url = reverse('authentication:login')

    email = 'milon@yopmail.com'
    password = 'milon123'

    def setUp(self):
        logging.getLogger('django').setLevel(logging.ERROR)
        self.user = User.objects.create_user(self.email, self.password)
        self.restaurant = Restaurant.objects.create(name='Test Restaurant', address='123 Test St')
        self.restaurant2 = Restaurant.objects.create(name='Test Restaurant 2', address='123 Test St')
        self.date = '2022-10-25'
        Menu.objects.create(restaurant=self.restaurant, date=self.date, item='Unique Test Menu')

    def _login(self):
        data = {
            'email': self.email, 'password': self.password
        }
        r = self.client.post(self.login_url, data)
        body = r.json()
        if 'access' in body:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer %s' % body['access'])
        return r.status_code, body

    def test_create_menu(self):
        self._login()
        url = reverse('restaurant:create_menu')
        data = {
            'restaurant': self.restaurant.id,
            'date': "2023-01-01",
            'item': 'New Item1,New Item2'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Menu.objects.filter(item='New Item1,New Item2').exists())

    def test_list_today_menu(self):
        self._login()
        url = reverse('restaurant:menu_list')
        today = timezone.now().date()
        self.menu1 = Menu.objects.create(restaurant=self.restaurant, date=today, item='Mutton,Chicken,Fish')
        self.menu2 = Menu.objects.create(restaurant=self.restaurant2, date=today, item='Vegetarian Dish')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_menu_unauthenticated(self):
        url = reverse('restaurant:create_menu')
        data = {
            'restaurant': self.restaurant.id,
            'date': str(timezone.now().date()),
            'item': 'New Item1,New Item2'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_menu_invalid_date(self):
        self._login()
        url = reverse('restaurant:create_menu')
        data = {
            'restaurant': self.restaurant.id,
            'date': '10-01-2023',
            'item': 'New Item1,New Item2'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_menu_uniqueness(self):
        with self.assertRaises(IntegrityError):
            Menu.objects.create(restaurant=self.restaurant, date=self.date, item='Duplicate Menu')

    def test_menu_non_uniqueness(self):
        Menu.objects.create(restaurant=self.restaurant2, date='2022-10-26', item='Another Menu')

        # Ensure that creating a menu with the same restaurant and a different date doesn't raise a IntegrityError
        Menu.objects.create(restaurant=self.restaurant2, date=self.date, item='Non-duplicate Menu')
