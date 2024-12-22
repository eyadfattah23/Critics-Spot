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

