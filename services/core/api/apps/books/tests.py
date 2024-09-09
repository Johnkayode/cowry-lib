from django.urls import reverse
from rest_framework.test import APITestCase
from api.apps.books.models import Book
from api.apps.users.models import User



class TestBook(APITestCase):
    """ Test module for the Book Model """
    
    def setUp(self):
        self.user = User.objects.create(
            email = "dwightschrute@theoffice.com",
            first_name = "Dwight",
            last_name = "Schrute",
        )
        self.book1 = Book.objects.create(
            title = "Book 1",
            author = "Author",
            publisher = "Publisher",
            category="fiction",
        )
        self.book2 = Book.objects.create(
            title = "Book 2",
            author = "Author",
            publisher = "Publisher 2",
            category="fiction",
        )

    def test_list_books(self):
        """Test that books can be listed and filtered"""
        url = reverse('list_books')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_filter_books_by_author(self):
        """Test filtering books by author"""
        url = reverse('list_books') + '?author=Author'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_filter_books_by_category(self):
        """Test filtering books by category"""
        url = reverse('list_books') + '?category=fiction'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_filter_books_by_publisher(self):
        """Test filtering books by publisher"""
        url = reverse('list_books') + '?publisher=Publisher'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['publisher'], 'Publisher')

    def test_retrieve_book(self):
        """Test that a book can be retrieved by its ID"""
        url = reverse('retrieve_book', kwargs={'uid': self.book1.uid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['title'], 'Book 1')

    def test_borrow_book(self):
        """Test that a book can be borrowed"""
        book = Book.objects.create(
            title = "New Book",
            author = "random",
            publisher = "Publisher 3",
            category="non-fiction",
        )
        url = reverse('create_book_borrow_request', kwargs={'uid': book.uid})
        data = {'user': str(self.user.uid), 'period': 7}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(book.is_unavailable, True)
