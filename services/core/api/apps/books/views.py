from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions as django_permissions, response, status
from api.apps.books.models import Book, BookBorrowRequest
from api.apps.books.serializers import BookSerializer, BookBorrowRequestSerializer


class ListBooksView(generics.ListAPIView):
    queryset = Book.objects.all()
    permission_classes = [django_permissions.AllowAny]
    serializer_class = BookSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "publisher",
        "category",
    ]


class RetrieveBookView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    permission_classes = [django_permissions.AllowAny]
    serializer_class = BookSerializer
    lookup_field = "uid"
    lookup_url_kwarg = "uid"


class CreateBookBorrowRequest(generics.CreateAPIView):
    queryset = BookBorrowRequest.objects.all()
    permission_classes = [django_permissions.AllowAny]
    serializer_class = BookBorrowRequestSerializer
    
    def create(self, request, uid, *args, **kwargs):
        request.data["book"] = uid
        return super().create(request, *args, **kwargs)
   
