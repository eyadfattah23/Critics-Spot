from django.test import TestCase
from .models import CustomUser, Favorite, BookReview, Book


class CustomUserTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username="testuser", email="testuser@example.com", password="testpassword")
        self.user.save()

    def test_user_creation(self):
        self.assertTrue(CustomUser.objects.filter(username="testuser").exists())

    def tearDown(self):
        CustomUser.objects.filter(username="testuser").delete()


class CustomBookReviewTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username="testuser", email="testuser@example.com", password="testpassword")
        self.user.save()
        self.book = Book.objects.create(title="testbook", buy_link="testlink", description="testdescription", pages=100, publication_date="2021-01-01")
        self.book.save()
        self.book_review = BookReview.objects.create(user=self.user, book=self.book, content="testcontent", rating=5)

    def test_book_review_creation(self):
        self.assertTrue(BookReview.objects.filter(user=self.user, book=self.book).exists())
        self.assertEqual(self.book_review.content, "testcontent")
        self.assertEqual(self.book_review.rating, 5)

    def tearDown(self):
        CustomUser.objects.filter(username="testuser").delete()
        Book.objects.filter(title="testbook").delete()

