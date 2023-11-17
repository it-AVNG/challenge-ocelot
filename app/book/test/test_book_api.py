'''
Test for book api
'''
from decimal import Decimal
import tempfile
import os

from PIL import Image

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Book
from book.serializers import BookSerializer, BookDetailSerializer


BOOKS_URL = reverse('book:book-list')


def detail_url(book_id):
    '''return a reverse book detail URL'''

    return reverse('book:book-detail', args=[book_id])


def create_user(**params):
    '''create and return a new user'''
    return get_user_model().objects.create_user(**params)


def image_upload_url(recipe_id):
    '''Create and return an image upload URL'''

    return reverse('book:book-upload-image', args=[recipe_id])


def create_book(user, **params):
    '''create and return sample book'''
    defaults = {
        'title': 'Sample Book title',
        'author': 'Sample author',
        'isbn': '1234567890123',
        'price': Decimal('4.40'),
    }

    defaults.update(params)

    book = Book.objects.create(user=user, **defaults)
    return book

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

    def test_get_book_detail(self):
        '''test for getting book details'''

        payload = {
            'email': 'test@example.com',
            'password': 'testpass@123',
            'name': 'Test Name2',
        }

        user = create_user(**payload)

        book = create_book(user=user)

        url = detail_url(book.id)

        res = self.client.get(url)
        serializer = BookDetailSerializer(book)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_auth_required_to_create_book(self):
        '''POST request is not allow for unauthorized'''

        payload = {
            'title': 'New Book title',
            'author': 'New author',
            'isbn': '1231234567890',
            'price': Decimal('5.50'),
        }

        res = self.client.post(BOOKS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

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

    def test_create_book(self):
        '''test creating a book'''
        payload = {
            'title': 'New Book title',
            'author': 'New author',
            'isbn': '1231234567890',
            'price': Decimal('5.50'),
        }

        res = self.client.post(BOOKS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        book = Book.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(book, k), v)

        self.assertEqual(book.user, self.user)

    def test_partial_update(self):
        '''partial update of a book'''

        add_description = 'only a test book'

        book = create_book(
            user=self.user,
            title='title sample',
            description=add_description,
        )

        payload = {'title': 'new editted title'}
        url = detail_url(book.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        book.refresh_from_db()
        self.assertEqual(book.title, payload['title'])
        self.assertEqual(book.description, add_description)
        self.assertEqual(book.user, self.user)

    def test_full_update_book(self):
        '''test full update of book'''

        book = create_book(
            user=self.user,
            title='Book Title',
            author='Old author',
            isbn='1234567890321',
            price=Decimal('5.5'),
            description='just testing description',
        )

        payload = {
            'title': 'Book Title',
            'author': 'Old author',
            'isbn': '1234567890321',
            'price': Decimal('2.30'),
            'description': 'just testing description',
        }

        url = detail_url(book.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        book.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(book, k), v)

        self.assertEqual(book.user, self.user)

    def test_update_user_return_error(self):
        '''test update user return error'''

        new_user = create_user(
            email='user2@example.com',
            password='testpass@123'
        )

        book = create_book(user=self.user)

        payload = {'user': new_user.id}

        url = detail_url(book.id)

        self.client.patch(url, payload)
        book.refresh_from_db()
        self.assertEqual(book.user, self.user)

    def test_delete_book_successful(self):
        '''test delete method for book'''

        book = create_book(user=self.user)

        url = detail_url(book.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=book.id).exists())

    def test_delete_other_user_book_error(self):
        '''Test trying to delete other user books gives error'''

        new_user = create_user(
            email='user2@example.com',
            password='testpass@123'
            )
        book = create_book(user=new_user)

        url = detail_url(book.id)
        self.client.delete(url)

        # self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Book.objects.filter(id=book.id).exists())

    def test_filter_by_author(self):
        '''Test filtering Book by author'''

        book1 = create_book(user=self.user,
                            title='NewBook test',
                            author='Book1 Author')
        book2 = create_book(user=self.user,
                            title='New2Book test2',
                            author='Book2 Authorin')
        book3 = create_book(user=self.user,
                            title='New3Book test3',
                            author='Book3 Authorinen')

        params = {'authors': f'{book1.author},{book2.author}'}
        res = self.client.get(BOOKS_URL, params)

        s1 = BookSerializer(book1)
        s2 = BookSerializer(book2)
        s3 = BookSerializer(book3)

        self.assertIn(s1.data, res.data)
        self.assertIn(s2.data, res.data)
        self.assertNotIn(s3.data, res.data)


class ImageUploadTests(TestCase):
    '''Test for Image upload API'''

    def setUp(self):
        self.client = APIClient()
        payload = {
            'email': 'test@example.com',
            'password': 'testpass@123',
            'name': 'Test Name',
        }
        self.user = create_user(**payload)
        self.client.force_authenticate(self.user)
        self.book = create_book(user=self.user)

    def tearDown(self):
        self.book.image.delete()

    def test_upload_image(self):
        '''Test upload an image to a book'''

        url = image_upload_url(self.book.id)

        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            img = Image.new('RGB', (10, 10))
            img.save(image_file, format='JPEG')

            image_file.seek(0)
            payload = {'image': image_file}

            res = self.client.post(url, payload, format='multipart')

        self.book.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertIn('image', res.data)
        self.assertTrue(os.path.exists(self.book.image.path))

    def test_upload_image_bad_request(self):
        '''Test upload invalid image'''

        url = image_upload_url(self.book.id)
        payload = {'image': 'notanimage'}

        res = self.client.post(url, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
