import json
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from api.apps.books.models import Book, BookBorrowRequest


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            "uid",
            "title",
            "author",
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
            "return_date",
        )
        read_only_fields = ("uid", "book", "request_date", "return_date")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        json_data = JSONRenderer().render(representation)
        return json.loads(json_data)
    
    def validate(self, attrs):
        book_uid = self.context.get("book_uid")
        try:
            book = Book.objects.get(uid=book_uid)
        except Book.DoesNotExist:
            raise serializers.ValidationError("Book with the provided UID does not exist.")
        if book.is_unavailable:
            raise serializers.ValidationError("Book is unavailable.")
        attrs["book"] = book

        return super().validate(attrs)
