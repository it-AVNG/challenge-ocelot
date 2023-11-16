'''
serializer for books apis
'''
from rest_framework import serializers

from core.models import Book


class BookSerializer(serializers.ModelSerializer):
    '''Serializer for books.'''

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'price', 'description']
        read_only_fields = ['id']