'''
Test for book api
'''
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Book
from book.serializers import BookSerializer


BOOKS_URL = reverse('book:book-list')

def create_user(**params):
    '''create and return a new user'''
    return get_user_model().objects.create_user(**params)

def create_book(user, **params):
    '''create and return sample book'''
    defaults = {
        'title': 'Sample Book title',
        'author': 'Sample author',
        'isbn': '1234567890123',
        'price': '4.40',
    }

    defaults.update(params)

    book = Book.objects.create(user=user, **defaults)

# public API test

class PublicBookAPITests(TestCase):
    '''Test unauthenticated API requests.'''

    def setUp(self):
        self.client = APIClient()

    def test_public_retrieve_book(self):
        '''Test connect to book list unauthentication success fully'''

        # create a user and user will make some books
        payload = {
            'email': 'test@example.com',
            'password': 'testpass@123',
            'name': 'Test Name2',
        }

        user = create_user(**payload)

        create_book(user=user)
        create_book(user=user)

        # retrieve data on book list
        res = self.client.get(BOOKS_URL)
        books = Book.objects.all().order_by('-id')
        serializer = BookSerializer(books, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(books.count(), 2)
        self.assertEqual(res.data, serializer.data)

    # def test_auth_required(self):
    #     '''Test auth is required to POST'''

    #     res = self.client.post(BOOK_ID_URL)

    #     self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

# private API test

class PrivateBookAPITests(TestCase):
    '''Test authenticated API request.'''

    def setUp(self):
        self.client = APIClient()
        payload = {
            'email': 'test@example.com',
            'password': 'testpass@123',
            'name': 'Test Name',
        }
        self.user = create_user(**payload)

        self.client.force_authenticate(self.user)

