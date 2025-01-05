from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTest(TestCase):
    """ Test User model. """
    def test_user_creation(self):
        user = User.objects.create_user(
            username="sampleuser",
            email="sampleuser@example.com",
            password="samplepassword"
        )
        self.assertEqual(user.username, "sampleuser")
        self.assertEqual(user.email, "sampleuser@example.com")
        self.assertTrue(user.check_password("samplepassword"))

    def test_superuser_creation(self):
        admin_user = User.objects.create_superuser(
            username="adminuser",
            email="adminuser@example.com",
            password="adminpassword"
        )
        self.assertEqual(admin_user.username, "adminuser")
        self.assertEqual(admin_user.email, "adminuser@example.com")
        self.assertTrue(admin_user.check_password("adminpassword"))
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
