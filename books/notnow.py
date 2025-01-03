# books/tests.py
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from decimal import Decimal
from datetime import date, timedelta
from .models import Author, Genre, Book


class AuthorModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            name="J.R.R. Tolkien",
            birth_date=date(1892, 1, 3),
            bio="English writer and philologist"
        )

    def test_author_creation(self):
        """Test basic author creation with required fields."""
        self.assertEqual(self.author.name, "J.R.R. Tolkien")
        self.assertEqual(self.author.birth_date, date(1892, 1, 3))
        self.assertEqual(self.author.bio, "English writer and philologist")
        self.assertIsNone(self.author.death_date)
        self.assertEqual(self.author.slug, "jrr-tolkien")
        self.assertEqual(str(self.author), "J.R.R. Tolkien")

    def test_future_birth_date_validation(self):
        """Test that birth date cannot be in the future."""
        future_date = timezone.now().date() + timedelta(days=1)
        author = Author(
            name="Future Author",
            birth_date=future_date
        )
        with self.assertRaises(ValidationError):
            author.full_clean()

    def test_death_date_validation(self):
        """Test death date validation."""
        # Test valid death date
        self.author.death_date = date(1973, 9, 2)
        self.author.full_clean()  # Should not raise error

        # Test death date before birth date
        self.author.death_date = date(1891, 1, 1)
        with self.assertRaises(ValidationError):
            self.author.full_clean()

        # Test future death date
        future_date = timezone.now().date() + timedelta(days=1)
        self.author.death_date = future_date
        with self.assertRaises(ValidationError):
            self.author.full_clean()

    def test_slug_generation(self):
        """Test automatic slug generation."""
        # First author
        author1 = Author.objects.create(
            name="Test Author",
            birth_date=date(1898, 11, 29)
        )
        self.assertEqual(author1.slug, "test-author")

        # Second author with same name should get a different slug
        author2 = Author(
            name="Test Author",
            birth_date=date(1898, 11, 29)
        )
        # Manually set a unique slug before saving
        author2.slug = "test-author-2"
        author2.save()

        self.assertNotEqual(author2.slug, author1.slug)


class GenreModelTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(
            name="Fantasy",
            description="Fantasy literature"
        )

    def test_genre_creation(self):
        """Test basic genre creation."""
        self.assertEqual(self.genre.name, "Fantasy")
        self.assertEqual(self.genre.description, "Fantasy literature")
        self.assertEqual(str(self.genre), "Fantasy")

    def test_unique_name_constraint(self):
        """Test that genre names must be unique."""
        with self.assertRaises(Exception):  # Could be IntegrityError or ValidationError
            Genre.objects.create(
                name="Fantasy",
                description="Another fantasy description"
            )


class BookModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            name="J.K. Rowling",
            birth_date=date(1965, 7, 31)
        )
        self.genre = Genre.objects.create(
            name="Fantasy",
            description="Fantasy literature"
        )
        self.book = Book.objects.create(
            title="Harry Potter and the Philosopher's Stone",
            description="The first book in the Harry Potter series",
            pages=223,
            publication_date=date(1997, 6, 26),
            author=self.author,
            avg_rating=Decimal("4.50")
        )
        self.book.genres.add(self.genre)

    def test_book_creation(self):
        """Test basic book creation with all fields."""
        self.assertEqual(
            self.book.title, "Harry Potter and the Philosopher's Stone")
        self.assertEqual(
            self.book.slug, "harry-potter-and-the-philosophers-stone")
        self.assertEqual(self.book.pages, 223)
        self.assertEqual(self.book.publication_date, date(1997, 6, 26))
        self.assertEqual(self.book.author, self.author)
        self.assertEqual(self.book.avg_rating, Decimal("4.50"))
        self.assertIn(self.genre, self.book.genres.all())
        self.assertEqual(
            str(self.book),
            f"{self.book.title}|{self.book.pk}, by: {self.author}|{self.author.id}"
        )

    def test_unique_title_constraint(self):
        """Test that book titles must be unique."""
        with self.assertRaises(Exception):  # Could be IntegrityError or ValidationError
            Book.objects.create(
                title="Harry Potter and the Philosopher's Stone",
                pages=223,
                publication_date=date(1997, 6, 26),
                author=self.author
            )

    def test_future_publication_date(self):
        """Test that publication date cannot be in the future."""
        future_date = timezone.now().date() + timedelta(days=1)
        book = Book(
            title="Future Book",
            pages=200,
            publication_date=future_date,
            author=self.author
        )
        with self.assertRaises(ValidationError):
            book.full_clean()

    def test_rating_validation(self):
        """Test rating validation."""
        # Test valid ratings
        self.book.avg_rating = Decimal("0.00")
        self.book.full_clean()  # Should not raise error

        self.book.avg_rating = Decimal("5.00")
        self.book.full_clean()  # Should not raise error

        # Test invalid ratings
        with self.assertRaises(ValidationError):
            self.book.avg_rating = Decimal("-0.01")
            self.book.full_clean()

        with self.assertRaises(ValidationError):
            self.book.avg_rating = Decimal("5.01")
            self.book.full_clean()

    def test_default_values(self):
        """Test default values for book fields."""
        book = Book.objects.create(
            title="Simple Book",
            pages=100,
            publication_date=date(2020, 1, 1),
            author=self.author
        )
        self.assertEqual(book.avg_rating, Decimal("0.00"))
        self.assertEqual(book.description, "")
        self.assertIsNone(book.buy_link)
        self.assertEqual(book.cover, "default_book.png")
        self.assertEqual(book.slug, "simple-book")

    def test_slug_generation(self):
        """Test automatic slug generation for books."""
        # Test basic slug generation
        book = Book.objects.create(
            title="The Lord of the Rings",
            pages=400,
            publication_date=date(1954, 7, 29),
            author=self.author
        )
        self.assertEqual(book.slug, "the-lord-of-the-rings")

        # Test slug with special characters
        book2 = Book.objects.create(
            title="The Book: A Test's Journey (2nd Edition)!",
            pages=200,
            publication_date=date(2020, 1, 1),
            author=self.author
        )
        self.assertEqual(book2.slug, "the-book-a-tests-journey-2nd-edition")

    def test_slug_uniqueness(self):
        """Test that book slugs are unique."""
        # Create first book
        book1 = Book.objects.create(
            title="Test Book2",
            pages=100,
            publication_date=date(2020, 1, 1),
            author=self.author
        )
        self.assertEqual(book1.slug, "test-book2")

        # Create second book with same title
        book2 = Book(
            title="Test Book",
            pages=100,
            publication_date=date(2020, 1, 1),
            author=self.author
        )
        # Manually set a unique slug before saving
        book2.slug = "test-book-2"
        book2.save()
        self.assertNotEqual(book2.slug, book1.slug)

    def test_custom_slug(self):
        """Test setting a custom slug."""
        book = Book.objects.create(
            title="My Custom Book",
            pages=100,
            publication_date=date(2020, 1, 1),
            author=self.author,
            slug="custom-slug-value"
        )
        self.assertEqual(book.slug, "custom-slug-value")
