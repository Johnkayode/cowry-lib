from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions as django_permissions, response, status
from api.apps.books.models import Book, BookBorrowRequest
from api.apps.books.serializers import BookSerializer, BookBorrowRequestSerializer
from rabbitmq import rabbitmq_client


class ListBooksView(generics.ListAPIView):
    queryset = Book.available_books()
    permission_classes = [django_permissions.AllowAny]
    serializer_class = BookSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "publisher",
        "category",
        "author",
    ]


class RetrieveBookView(generics.RetrieveAPIView):
    queryset = Book.available_books()
    permission_classes = [django_permissions.AllowAny]
    serializer_class = BookSerializer
    lookup_field = "uid"
    lookup_url_kwarg = "uid"


class CreateBookBorrowRequest(generics.CreateAPIView):
    queryset = BookBorrowRequest.objects.all()
    permission_classes = [django_permissions.AllowAny]
    serializer_class = BookBorrowRequestSerializer
    
    def create(self, request, uid, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"book_uid": uid})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        rabbitmq_client.publish("admin_updates", {"event_type": "book.borrowed", "data": serializer.data})

        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    
   
