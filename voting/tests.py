import logging

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.urls import reverse
from django.utils import timezone

from rest_framework.test import APITestCase
from rest_framework import status

from voting.models import Voting
from restaurant.models import Restaurant, Menu

User = get_user_model()


class VotingViewSetTestCase(APITestCase):
    login_url = reverse('authentication:login')

    email = 'milon@yopmail.com'
    password = 'milon123'

    def setUp(self):
        logging.getLogger('django').setLevel(logging.ERROR)
        self.user = User.objects.create_user(self.email, self.password)

        self.restaurant = Restaurant.objects.create(name='Test Restaurant 1', address='123 Test St')
        self.restaurant2 = Restaurant.objects.create(name='Test Restaurant 2', address='123 Test St')
        self.restaurant3 = Restaurant.objects.create(name='Test Restaurant 3', address='123 Test St')
        self.date = '2023-10-25'
        self.menu = Menu.objects.create(restaurant=self.restaurant, date=timezone.now().date(), item='Menu Item 1')
        self.menu2 = Menu.objects.create(restaurant=self.restaurant2, date='2023-10-23', item='Menu Item 2')
        self.menu3 = Menu.objects.create(restaurant=self.restaurant3, date='2022-10-22', item='Menu Item 3')

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

    def test_create_vote(self):
        self._login()
        url = reverse('voting:create_voting')

        data = {
            'menu': self.menu.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Voting.objects.filter(user=self.user, menu=self.menu).exists())

    def test_list_votes(self):
        self._login()
        url = reverse('voting:voting_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(Voting.objects.get_votes_for_today_menus()))

    def test_create_vote_unauthenticated(self):
        url = reverse('voting:create_voting')
        data = {
            'menu': self.menu2.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_duplicate_vote(self):
        self._login()
        url = reverse('voting:create_voting')
        data = {
            'menu': self.menu3.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        with self.assertRaises(IntegrityError):
            Voting.objects.create(menu=self.menu3, user=self.user)

    def test_create_vote_for_invalid_menu(self):
        self._login()
        url = reverse('voting:create_voting')
        data = {
            'user': self.user.id,
            'menu': self.menu3.id + 1,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
