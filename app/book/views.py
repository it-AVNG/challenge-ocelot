'''
Views for the Book API
'''
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from core.models import Book
from book import serializers
from book.permissions import IsOwnerOrReadonly

class BookViewSet(viewsets.ModelViewSet):
    '''View for manage book APIs'''

    serializer_class = serializers.BookDetailSerializer
    queryset = Book.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadonly]

    def get_queryset(self):
        '''retrive books'''

        return self.queryset.order_by('-id')

    def get_serializer_class(self):
        '''return the serializer class for request'''

        if self.action == 'list':
            return serializers.BookSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        '''create new book'''

        serializer.save(user=self.request.user)