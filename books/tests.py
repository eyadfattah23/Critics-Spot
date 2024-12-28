from rest_framework.test import APITestCase
from rest_framework import status
from django.test import TestCase
from .models import *


class AuthorModelTest(TestCase):

    def setUp(self):
        self.author = Author.objects.create(
            name="J.R.R. Tolkien",
            birth_date="1892-01-03"
        )

    def test_author_creation(self):
        self.assertEqual(self.author.name, "J.R.R. Tolkien")
        self.assertEqual(str(self.author), "J.R.R. Tolkien")
        self.assertEqual(self.author.birth_date, "1892-01-03")


class GenreModelTest(TestCase):

    def setUp(self):
        self.genre = Genre.objects.create(
            name="Fantasy",
            description="A genre of speculative fiction."
        )

    def test_genre_creation(self):
        self.assertEqual(self.genre.name, "Fantasy")
        self.assertEqual(self.genre.description,
                         "A genre of speculative fiction.")
        self.assertEqual(str(self.genre), "Fantasy")


class BookModelTest(TestCase):

    def setUp(self):
        self.author = Author.objects.create(
            name="J.R.R. Tolkien",
            birth_date="1892-01-03"
        )
        self.genre = Genre.objects.create(
            name="Fantasy",
            description="A genre of speculative fiction."
        )
        self.book = Book.objects.create(
            title="The Hobbit",
            description="A fantasy novel by J.R.R. Tolkien.",
            author=self.author,
            publication_date="1937-09-21",
            pages=310
        )
        self.book.genres.add(self.genre)

    def test_book_creation(self):
        self.assertEqual(self.book.title, "The Hobbit")
        self.assertEqual(self.book.description,
                         "A fantasy novel by J.R.R. Tolkien.")
        self.assertEqual(self.book.author, self.author)
        self.assertEqual(self.book.pages, 310)
        self.assertEqual(self.book.publication_date, "1937-09-21")
        self.assertIn(self.genre, self.book.genres.all())

    def test_book_str_representation(self):
        self.assertEqual(
            str(self.book), f"The Hobbit|{self.book.pk}, by: {self.author.name}|{self.author.pk}")


class AuthorAPITest(APITestCase):
    def setUp(self):
        self.author = Author.objects.create(
            name="J.R.R. Tolkien", birth_date="1892-01-03")

    def test_get_authors(self):
        response = self.client.get("/api/authors/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "J.R.R. Tolkien")

    def test_create_author(self):
        data = {"name": "George R.R. Martin", "birth_date": "1948-09-20"}
        response = self.client.post("/api/authors/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "George R.R. Martin")

    def test_invalid_author_creation(self):
        data = {"name": ""}
        response = self.client.post("/api/authors/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GenreAPITest(APITestCase):
    def setUp(self):
        self.genre = Genre.objects.create(
            name="Fantasy", description="A fantasy genre.")

    def test_get_genres(self):
        response = self.client.get("/api/genres/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Fantasy")

    def test_create_genre(self):
        data = {"name": "Science Fiction", "description": "A sci-fi genre."}
        response = self.client.post("/api/genres/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "Science Fiction")

    def test_genre_details(self):
        response = self.client.get(f"/api/genres/{self.genre.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Fantasy")


class BookAPITest(APITestCase):
    def setUp(self):
        self.author = Author.objects.create(
            name="J.R.R. Tolkien", birth_date="1892-01-03")
        self.genre = Genre.objects.create(
            name="Fantasy", description="A fantasy genre.")
        self.book = Book.objects.create(
            title="The Hobbit",
            author=self.author,
            pages=310,
            description="A fantasy novel.",
            publication_date="1937-09-21"
        )
        self.book.genres.add(self.genre)

    def test_get_books(self):
        response = self.client.get("/api/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "The Hobbit")

    def test_create_book(self):
        data = {
            "title": "The Silmarillion",
            "description": "A prequel to The Hobbit.",
            "author": self.author.id,
            "genres": [self.genre.id],
            "publication_date": "1977-09-15",
            "pages": 365,
        }
        response = self.client.post("/api/books/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "The Silmarillion")

    def test_book_details(self):
        response = self.client.get(f"/api/books/{self.book.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "The Hobbit")
