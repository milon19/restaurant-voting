import logging

from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status

from user.models import Employee

User = get_user_model()


class CreateEmployeeAPITestCase(APITestCase):
    api_url = reverse('user:create_employee')

    def setUp(self):
        logging.getLogger('django').setLevel(logging.ERROR)

    def test_create_employee(self):

        data = {
            'first_name': 'Milon',
            'last_name': 'Mahato',
            'email': 'milon@example.com',
            'password': 'my_secure_password'
        }

        response = self.client.post(self.api_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='milon@example.com').exists())
        self.assertTrue(Employee.objects.filter(first_name='Milon', last_name='Mahato').exists())

    def test_create_employee_with_existing_email(self):
        User.objects.create_user(email='existing@example.com', password='testpassword')

        data = {
            'first_name': 'Milon',
            'last_name': 'Mahato',
            'email': 'existing@example.com',
            'password': 'another_password'
        }

        response = self.client.post(self.api_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(User.objects.filter(email='existing@example.com').exists())

    def test_create_employee_with_missing_data(self):
        data = {
            'first_name': 'Incomplete',
            'last_name': 'Data',
        }

        response = self.client.post(self.api_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Employee.objects.filter(first_name='Incomplete', last_name='Data').exists())

    def test_create_employee_with_invalid_email(self):
        data = {
            'first_name': 'Invalid',
            'last_name': 'Email',
            'email': 'invalid_email',  # Invalid email format
            'password': 'password123'
        }

        response = self.client.post(self.api_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Employee.objects.filter(first_name='Invalid', last_name='Email').exists())
