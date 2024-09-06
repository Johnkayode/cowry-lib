from rest_framework import serializers
from api.apps.books.models import Book, BookBorrowRequest


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            "uid",
            "title",
            "publisher",
            "category",
            "created_at"
        )
        read_only_fields = ("uid", "created_at",)


class BookBorrowRequestSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BookBorrowRequest
        fields = (
            "uid",
            "user",
            "book",
            "period",
            "request_date",
        )
        read_only_fields = ("uid", "request_date")