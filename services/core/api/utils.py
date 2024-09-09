from api.apps.books.models import Book

def process_message(event: str, data: str):
    print(event, data)
    if event == "book.created":
        try:
            book = Book.objects.get(uid=data["uid"])
        except Book.DoesNotExist:
            Book.objects.create(
                **data
            )
            print("Book created")
    elif event == "book.deleted":
        try:
            book = Book.objects.get(uid=data["uid"])
            book.soft_delete()
            print("Book deleted")
        except Book.DoesNotExist:
            pass
        