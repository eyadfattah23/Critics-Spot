from django.test import TestCase
from .models import Book, Genre, Author
import datetime

class GenreTestCase(TestCase):
    """ Test the author class. """
    def setUp(self):
        # Create a genre for testing
        self.genre = Genre.objects.create(name="Fiction", description="A book that is not real.", added_date=datetime.datetime.now())
        self.genre.save()
    
    def test_genre_creation(self):
        # Test if the genre was created
        self.assertTrue(Genre.objects.filter(name="Fiction").exists())
    
    def tearDown(self):
        # Delete the genre after testing
        self.genre.delete()


class AuthorTestCase(TestCase):
    """ Test the author class. """
    def setUp(self):
        # Create an author for testing
        self.author = Author.objects.create(name="MoAli", birth_date=datetime.datetime.now(), death_date=datetime.datetime.now(), bio="A great author", photo="default_author.png", added_date=datetime.datetime.now())
        self.author.save()

    def test_author_creation(self):
        # Test if the author was created
        self.assertTrue(Author.objects.filter(name="MoAli").exists())
    
    def tearDown(self):
        # Delete the author after testing
        self.author.delete()

class BookTestCase(TestCase):
    """ Test the book class. """
    def setUp(self):
        # Create an author for testing
        self.author = Author.objects.create(name="MoAli", birth_date=datetime.datetime.now(), death_date=datetime.datetime.now(), bio="A great author", photo="default_author.png", added_date=datetime.datetime.now())
        self.author.save()
        self.book = Book.objects.create(title="How Did I Became a Billionaire", buy_link="MoThepharoahBook.com", description="A book that tells the story of how I became a billionaire", pages=200, publication_date=datetime.datetime.now(), added_date=datetime.datetime.now(), cover="default_book.png", author=self.author)
        self.genre1 = Genre.objects.create(name="Biography", description="A book that tells the story of someone's life", added_date=datetime.datetime.now())
        self.genre2 = Genre.objects.create(name="self-Development", description="A book that tells gives people tips to be better.", added_date=datetime.datetime.now())
        self.genre1.save()
        self.genre2.save()        
        self.book.genres.add(self.genre1, self.genre2)
        self.book.save()

    def test_book_creation(self):
        # Test if the book was created
        self.assertTrue(Book.objects.filter(title="How Did I Became a Billionaire").exists())
        self.assertTrue(Author.objects.filter(name="MoAli").exists())
        self.assertTrue(Genre.objects.filter(name="Biography").exists())
        self.assertTrue(Genre.objects.filter(name="self-Development").exists())
        self.assertIn(self.genre1, self.book.genres.all())
        self.assertIn(self.genre2, self.book.genres.all())
    
    def tearDown(self):
        # Delete the book after testing
        self.book.genres.clear()
        self.genre1.delete()
        self.genre2.delete()
        self.book.delete()
        self.author.delete()
