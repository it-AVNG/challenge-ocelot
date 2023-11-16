'''
Views for the Book API
'''
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from core.models import Book
from book import serializers


class BookViewSet(viewsets.ModelViewSet):
    '''View for manage book APIs'''

    serializer_class = serializers.BookSerializer
    queryset = Book.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        '''retrive books'''

        return self.queryset.order_by('-id')
