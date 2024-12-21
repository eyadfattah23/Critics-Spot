from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Shelf, ShelfBook
from books.models import Book

User = get_user_model()


class ShelfModelTest(TestCase):
    """ Test Shelf model. """
    def test_shelf_creation(self):
        user = User.objects.create_user(
            username="sampleuser",
            password="samplepassword"
        )
        shelf = Shelf.objects.create(
            name="Read",
            user=user,
            is_default=True
        )
        self.assertEqual(shelf.name, "Read")
        self.assertEqual(shelf.user.username, "sampleuser")
        self.assertTrue(shelf.is_default)


class ShelfBookModelTest(TestCase):
    """ Test ShelfBook model. """
    def test_shelf_book_creation(self):
        user = User.objects.create_user(
            username="sampleuser",
            password="samplepassword"
        )
        shelf = Shelf.objects.create(
            name="Read",
            user=user,
            is_default=True
        )
        book = Book.objects.create(
            title="Sample Book",
            author="Sample Author",
            isbn="1234567890",
            publication_date="2023-01-01"
        )
        shelf_book = ShelfBook.objects.create(
            shelf=shelf,
            book=book
        )
        self.assertEqual(shelf_book.shelf.name, "Read")
        self.assertEqual(shelf_book.book.title, "Sample Book")
