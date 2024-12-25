from django.test import TestCase
from books.models import Book, Author, Genre
from groups.models import Group, Like, Comment, Post
from shelves.models import Shelf, ShelfBook
from users.models import CustomUser, Favorite, BookReview

class TestRelatios(TestCase):
    """Test the relation between models."""
    
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', email='testemail@user.com', password='testpassword')
        