from django.urls import path
from api.apps.books import views


urlpatterns = [
    path("", views.ListBooksView.as_view(), name="list_books"),
    path("<uuid:uid>/", views.RetrieveBookView.as_view(), name="retrieve_book"),
    path("<uuid:uid>/borrow/", views.CreateBookBorrowRequest.as_view(), name="create_book_borrow_request"),
]