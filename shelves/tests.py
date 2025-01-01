from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from datetime import date
from decimal import Decimal

from books.models import Book, Author, Genre
from shelves.models import Shelf, ShelfBook

User = get_user_model()


class AuthorModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            name="Test Author",
            birth_date=date(1990, 1, 1),
            bio="Test bio"
        )

    def test_author_creation(self):
        self.assertEqual(str(self.author), "Test Author")
        self.assertEqual(self.author.birth_date, date(1990, 1, 1))
        self.assertEqual(self.author.bio, "Test bio")
        self.assertIsNone(self.author.death_date)


class GenreModelTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(
            name="Fiction",
            description="Test description"  # Making sure we always provide a description
        )

    def test_genre_creation(self):
        self.assertEqual(str(self.genre), "Fiction")
        self.assertEqual(self.genre.description, "Test description")

    def test_unique_name_constraint(self):
        with self.assertRaises(IntegrityError):
            Genre.objects.create(
                name="Fiction",
                description="Another description"  # Adding description here too
            )


class BookModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            name="Test Author",
            birth_date=date(1990, 1, 1)
        )
        self.genre = Genre.objects.create(
            name="Fiction",
            description="Test genre description"  # Added description
        )
        self.book = Book.objects.create(
            title="Test Book",
            pages=200,
            publication_date=date(2020, 1, 1),
            author=self.author,
            avg_rating=Decimal("4.50")
        )
        self.book.genres.add(self.genre)

    def test_book_creation(self):
        self.assertEqual(
            str(self.book), f"Test Book|{self.book.pk}, by: Test Author|{self.author.id}")
        self.assertEqual(self.book.pages, 200)
        self.assertEqual(self.book.avg_rating, Decimal("4.50"))

    def test_unique_title_constraint(self):
        with self.assertRaises(IntegrityError):
            Book.objects.create(
                title="Test Book",
                pages=200,
                publication_date=date(2020, 1, 1),
                author=self.author
            )

    def test_rating_validation(self):
        with self.assertRaises(ValidationError):
            self.book.avg_rating = Decimal("5.01")
            self.book.full_clean()

        with self.assertRaises(ValidationError):
            self.book.avg_rating = Decimal("-0.01")
            self.book.full_clean()


class ShelfModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.shelf = Shelf.objects.create(
            name="Test Shelf",
            user=self.user
        )

    def test_shelf_creation(self):
        self.assertEqual(
            str(self.shelf),
            f'shelf "Test Shelf":{self.shelf.pk} owned by "testuser":{self.user.pk}'
        )

    def test_unique_name_per_user_constraint(self):
        with self.assertRaises(IntegrityError):
            Shelf.objects.create(
                name="Test Shelf",
                user=self.user
            )

    def test_default_shelves(self):
        self.assertEqual(Shelf.DEFAULT_SHELVES, [
                         'Read', 'Currently Reading', 'Want To Read', 'Favorites'])


class ShelfBookModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.shelf = Shelf.objects.create(
            name="Test Shelf",
            user=self.user
        )
        self.author = Author.objects.create(
            name="Test Author",
            birth_date=date(1990, 1, 1)
        )
        self.book = Book.objects.create(
            title="Test Book",
            pages=200,
            publication_date=date(2020, 1, 1),
            author=self.author
        )
        self.shelf_book = ShelfBook.objects.create(
            shelf=self.shelf,
            book=self.book,
            current_page=50
        )

    def test_shelf_book_creation(self):
        self.assertEqual(
            str(self.shelf_book),
            f"Test Book|{self.book.id} in Test Shelf|{self.shelf.id} owned by user: (testuser)|{self.user.id}"
        )
        self.assertEqual(self.shelf_book.current_page, 50)

    def test_unique_book_per_shelf_constraint(self):
        with self.assertRaises(IntegrityError):
            ShelfBook.objects.create(
                shelf=self.shelf,
                book=self.book
            )

    def test_current_page_validation(self):
        # Test that current_page cannot be negative (handled by PositiveIntegerField)
        with self.assertRaises(IntegrityError):
            ShelfBook.objects.create(
                shelf=self.shelf,
                book=Book.objects.create(
                    title="Another Book",
                    pages=200,
                    publication_date=date(2020, 1, 1),
                    author=self.author
                ),
                current_page=-1
            )
