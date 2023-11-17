'''
Views for the Book API
'''
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
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
        elif self.action == 'upload_image':
            return serializers.BookImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        '''create new book'''

        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        '''Upload image to a book'''

        book = self.get_object()
        serializer = self.get_serializer(book, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
