'''
tests for models
'''
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


class ModelTests(TestCase):
    ''' Test models'''

    def test_create_user_with_email_successful(self):
        '''Test creating a user with an email is successful'''
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        '''Test email is normalized for new users.'''

        sample_email = [
            ['test1@ExamPle.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.com', 'test4@example.com'],
        ]

        for email, expected in sample_email:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        '''Test that creating user without an email raise ValueError'''

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        '''test create a superuser'''

        user = get_user_model().objects.create_superuser(
            'testsuper@example.com',
            'supertest123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_book(self):
        '''test create book successful'''

        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass@123',
        )

        book = models.Book.objects.create(
            user=user,
            title='Sample Book title',
            author='Sample Author',
            price=Decimal('5.50'),
            isbn='1234567890123',
        )

        self.assertEqual(str(book), book.title)