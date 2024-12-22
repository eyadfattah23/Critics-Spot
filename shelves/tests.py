from django.test import TestCase
from .models import Shelf, ShelfBook
from users.models import CustomUser
from books.models import Book, Author
import datetime


class ShelfTestCase(TestCase):
    """ Test the shelf model """
    def setUp(self):
        """ Create a shelf """
        self.user = CustomUser.objects.create_user(username='testuser', email='testemail@user.com', password='12345')
        self.shelf = Shelf.objects.create(name="My Shelf", user=self.user, is_default=False)

    def test_shelf_creation(self):
        """ Test shelf creation """
        self.assertEqual(self.shelf.name, "My Shelf")
        self.assertEqual(self.shelf.user, self.user)
        self.assertEqual(self.shelf.is_default, False)

    def test_shelf_str_representation(self):
        """ Test shelf string representation """
        self.assertEqual(str(self.shelf), f"shelf: My Shelf owned by ({self.user.username})")

    def tearDown(self):
        """ Delete the shelf """
        self.user.delete()
        self.shelf.delete()


class ShelfBookTestCase(TestCase):
    """ Test the shelf book model """
    def setUp(self):
        """ Create a shelf book """
        self.user = CustomUser.objects.create_user(username='testuser', email='testemail', password='12345')
        self.shelf = Shelf.objects.create(name="My Shelf", user=self.user, is_default=False)
        self.author = Author.objects.create(name="MoAli", birth_date=datetime.datetime.now(), death_date=datetime.datetime.now(), bio="A great author", photo="default_author.png", added_date=datetime.datetime.now())
        self.book = Book.objects.create(title="How Did I Became a Billionaire", buy_link="MoThepharoahBook.com", description="A book that tells the story of how I became a billionaire", pages=200, publication_date=datetime.datetime.now(), added_date=datetime.datetime.now(), cover="default_book.png", author=self.author)
        self.shelf_book = ShelfBook.objects.create(shelf=self.shelf, book=self.book)
    def test_shelf_book_creation(self):
        """ Test shelf book creation """
        self.assertEqual(self.shelf.name, "My Shelf")
        self.assertEqual(self.shelf.user, self.user)
        self.assertEqual(self.shelf_book.shelf, self.shelf)
        self.assertEqual(self.shelf_book.book, self.book)


    def tearDown(self):
        """ Delete the shelf book """
        self.user.delete()
        self.shelf.delete()
        self.book.delete()
        self.author.delete()
        self.shelf_book.delete()
