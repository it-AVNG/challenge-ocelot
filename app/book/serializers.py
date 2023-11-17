'''
serializer for books apis
'''
from rest_framework import serializers

from core.models import Book


class BookSerializer(serializers.ModelSerializer):
    '''Serializer for books.'''

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'price', 'publish_date']
        read_only_fields = ['id']


class BookDetailSerializer(BookSerializer):
    '''Serializer for book detail view'''

    user = serializers.ReadOnlyField(source='user.username')

    class Meta(BookSerializer.Meta):
        fields = BookSerializer.Meta.fields + ['description', 'user']
