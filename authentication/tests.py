from datetime import timedelta
from functools import partial
from unittest import mock

from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.utils import aware_utcnow

User = get_user_model()


class TestAuthenticationCase(APITestCase):

    login_url = reverse('authentication:login')
    refresh_token_url = reverse('authentication:token_refresh')
    logout_url = reverse('authentication:logout')
    auth_user_details_url = reverse('user:auth_user')

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

    def test_login_success_response_200(self):
        status, body = self._login()
        self.assertEquals(status, 200)
        self.assertIn('access', body.keys())
        self.assertIn('refresh', body.keys())

    def test_logout_response_200(self):
        _, body = self._login()
        data = {'refresh': body['refresh']}
        r = self.client.post(self.logout_url, data)
        self.assertEquals(r.status_code, 200)

    def test_logout_with_bad_refresh_token_response_400(self):
        self._login()
        data = {'refresh': 'dsf.sdfsdf.sdf'}
        r = self.client.post(self.logout_url, data)
        body = r.json()
        test_response = {'detail': 'Token is invalid or expired', 'code': 'token_not_valid'}
        self.assertEquals(r.status_code, 401)
        self.assertTrue(body, test_response)

    def test_logout_refresh_token_in_blacklist(self):
        _, body = self._login()
        r = self.client.post(self.logout_url, body)
        token = partial(RefreshToken, body['refresh'])
        self.assertRaises(TokenError, token)

    def test_access_token_still_valid_after_logout(self):
        _, body = self._login()
        self.client.post(self.logout_url, body)
        r = self.client.get(self.auth_user_details_url)
        body = r.json()
        self.assertEquals(r.status_code, 200, body)
        self.assertTrue(body, body)

    def test_access_token_invalid_in_7days_after_logout(self):
        _, body = self._login()
        self.client.post(self.logout_url, body)
        m = mock.Mock()
        m.return_value = aware_utcnow() + timedelta(days=7)
        with mock.patch('rest_framework_simplejwt.tokens.aware_utcnow', m):
            r = self.client.get(self.auth_user_details_url)
            body = r.json()
        self.assertEquals(r.status_code, 401, body)
        self.assertTrue(body, body)

    def test_refresh_token_success_response_200(self):
        status, body = self._login()
        r = self.client.post(self.refresh_token_url, {"refresh": body['refresh']})
        res = r.json()
        self.assertEquals(r.status_code, 200, body)
        self.assertIn('access', res.keys())
        self.assertIn('refresh', res.keys())

    def test_refresh_token_wrong_token_type(self):
        status, body = self._login()
        r = self.client.post(self.refresh_token_url, {"refresh": body['access']})
        res = r.json()
        self.assertEquals(r.status_code, 401, body)
        self.assertEquals(res, {'detail': 'Token has wrong type', 'code': 'token_not_valid'})

    def test_refresh_token_failed_after_logout(self):
        status, body = self._login()
        self.client.post(self.logout_url, {"refresh": body['refresh']})
        r = self.client.post(self.refresh_token_url, {"refresh": body['refresh']})
        res = r.json()
        self.assertEquals(r.status_code, 401, body)
        self.assertEquals(res, {'code': 'token_not_valid', 'detail': 'Token is blacklisted'})
