'''
test for user API
'''
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    '''create and return a new user'''
    return get_user_model().objects.create_user(**params)

# Public test -Unauthenticated request


class PublicUserApiTest(TestCase):
    '''Test the public features of the user API.'''

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        '''Test create a user is successfull'''

        payload = {
            'email': 'test@example.com',
            'password': 'test@123',
            'name': 'Test Name',
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))

        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        '''Test if user with email exists.'''

        payload = {
            'email': 'test@example.com',
            'password': 'testpass@123',
            'name': 'Test Name2',
        }

        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        '''Test error is return for password less then 5 char.'''

        payload = {
            'email': 'test@example.com',
            'password': 'pw12',
            'name': 'Test Name3',
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        '''test generates token for valid users'''

        user_details = {
            'name': 'Test Name',
            'email': 'test@example.com',
            'password': 'test-user-password123',
        }

        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': user_details['password']
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)

    def test_create_token_bad_credentials(self):
        '''test returns error if credentials invalid'''

        create_user(email='test@example.com', password='goodpass')

        payload = {
            'email': 'test@example.com',
            'password': 'badpass'
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_create_token_blank_password(self):
        '''Test posting blank password returns error'''

        payload = {'email': 'test@example.com', 'password': ''}
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_retrieve_user_unauthorized(self):
        '''Test authentication is required for users'''

        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


# Private test - authenticated test to endpoints

class PrivateUserApiTest(TestCase):
    '''Test API requests that require authentication'''

    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            password='testpass@123',
            name='test name',
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        '''test retrieving profile for logged in user'''

        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email,
        })

    def test_post_me_not_allowed(self):
        '''Test POST request is not allow for the me endpoint'''

        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        '''test updating user profile for the authenticated user'''

        payload = {
            'name': 'Updated Name',
            'password': 'newpassword123'
        }

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
