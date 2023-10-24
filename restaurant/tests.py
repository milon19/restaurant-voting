from django.contrib.auth import get_user_model

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from restaurant.models import Restaurant

User = get_user_model()


class RestaurantViewSetTestCase(APITestCase):
    login_url = reverse('authentication:login')

    email = 'milon@yopmail.com'
    password = 'milon123'

    def setUp(self):
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
