from django.test import TestCase
from .models import Book, Genre, Author


class AuthorModelTest(TestCase):
    """ Class for testing author models. """
    def test_author_creation(self):
        author = Author.objects.create(
            name="Sample Author",
            birth_date="1970-01-01",
            bio="This is a sample author."
        )
        self.assertEqual(author.name, "Sample Author")
        self.assertEqual(author.birth_date, "1970-01-01")
        self.assertEqual(author.bio, "This is a sample author.")


class GenreModelTest(TestCase):
    """ Class for testing genre models. """
    def test_genre_creation(self):
        genre = Genre.objects.create(
            name="Sample Genre",
            description="This is a sample genre."
        )
        self.assertEqual(genre.name, "Sample Genre")
        self.assertEqual(genre.description, "This is a sample genre.")


class BookModelTest(TestCase):
    """ Class for testing book models. """
    def test_book_creation(self):
        author = Author.objects.create(
            name="Sample Author",
            birth_date="1970-01-01",
            bio="This is a sample author."
        )
        book = Book.objects.create(
            title="Sample Book",
            author=author,
            publication_date="2023-01-01"
        )
        self.assertEqual(book.title, "Sample Book")
        self.assertEqual(book.author.name, "Sample Author")
        self.assertEqual(book.publication_date, "2023-01-01")
