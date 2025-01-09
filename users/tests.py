#!/usr/bin/pytho3n
"""Tests for the users app."""
import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from users.models import CustomUser
from users.serializers import UserProfileSerializer


@pytest.fixture
def create_user():
    """Create a test user.

    Returns:
        function: Factory function to create test users.
    """
    def make_user(username='testuser', email='test@example.com', password='testpass123', is_staff=False):
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_staff=is_staff
        )
        return user
    return make_user


@pytest.mark.django_db
class TestUserRegistration:
    """Test cases for user registration functionality."""

    def test_user_registration(self):
        """Test successful user registration with valid data."""
        client = APIClient()
        url = reverse('users-list')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'securepass123',
            'password_confirm': 'securepass123'
        }
        response = client.post(url, data, format='json')
        assert response.status_code == 201
        assert CustomUser.objects.filter(email='newuser@example.com').exists()

    def test_invalid_registration(self):
        """Test registration with mismatched passwords."""
        client = APIClient()
        url = reverse('users-list')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'securepass123',
            'password_confirm': 'differentpass123'
        }
        response = client.post(url, data, format='json')
        assert response.status_code == 400
        assert 'password' in response.data


@pytest.mark.django_db
class TestUserProfile:
    """Test cases for user profile management."""

    def test_retrieve_profile(self, create_user):
        """Test retrieving user profile."""
        user = create_user()
        client = APIClient()
        client.force_authenticate(user=user)
        url = reverse('users-me')
        response = client.get(url)
        assert response.status_code == 200
        assert response.data['email'] == user.email
        assert response.data['username'] == user.username

    def test_update_profile(self, create_user):
        """Test updating user profile information."""
        user = create_user()
        client = APIClient()
        client.force_authenticate(user=user)
        url = reverse('users-me')
        data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'bio': 'New bio'
        }
        response = client.patch(url, data, format='json')
        assert response.status_code == 200
        assert response.data['first_name'] == 'Updated'
        assert response.data['last_name'] == 'Name'

    def test_upload_profile_image(self, create_user):
        """Test uploading profile image."""
        user = create_user()
        client = APIClient()
        client.force_authenticate(user=user)
        url = reverse('users-me')
        image = SimpleUploadedFile(
            "test_image.jpg", b"file_content", content_type="image/jpeg"
        )
        data = {'image': image}
        response = client.patch(url, data, format='multipart')
        assert response.status_code == 200
        assert 'image' in response.data


@pytest.mark.django_db
class TestUserPermissions:
    """Test cases for user permissions and authorization."""

    def test_unauthorized_access(self):
        """Test accessing protected endpoints without authentication."""
        client = APIClient()
        url = reverse('users-me')
        response = client.get(url)
        assert response.status_code == 401

    def test_admin_access(self, create_user):
        """Test admin user access to protected endpoints."""
        admin = create_user(
            username='admin', email='admin@example.com', is_staff=True
        )
        client = APIClient()
        client.force_authenticate(user=admin)
        url = reverse('users-list')
        response = client.get(url)
        assert response.status_code == 200

    def test_user_list_restriction(self, create_user):
        """Test regular user cannot access user list."""
        user = create_user()
        client = APIClient()
        client.force_authenticate(user=user)
        url = reverse('users-list')
        response = client.get(url)
        assert response.status_code == 403


@pytest.mark.django_db
class TestUserDeletion:
    """Test cases for user account deletion."""

    def test_delete_own_account(self, create_user):
        """Test user can delete their own account."""
        user = create_user()
        client = APIClient()
        client.force_authenticate(user=user)
        url = reverse('users-me')
        response = client.delete(url)
        assert response.status_code == 204
        assert not CustomUser.objects.filter(email=user.email).exists()

    def test_admin_delete_user(self, create_user):
        """Test admin can delete other user accounts."""
        admin = create_user(
            username='admin', email='admin@example.com', is_staff=True
        )
        user = create_user(
            username='userdelete', email='delete@example.com'
        )
        client = APIClient()
        client.force_authenticate(user=admin)
        url = reverse('users-detail', args=[user.id])
        response = client.delete(url)
        assert response.status_code == 204
        assert not CustomUser.objects.filter(email=user.email).exists()


@pytest.mark.django_db
class TestUserSerialization:
    """Test cases for user serialization."""

    def test_user_profile_serialization(self, create_user):
        """Test UserProfileSerializer output."""
        user = create_user()
        serializer = UserProfileSerializer(user, context={'request': None})
        data = serializer.data
        assert data['username'] == user.username
        assert data['email'] == user.email
        assert 'password' not in data
        assert 'shelves' in data


@pytest.mark.django_db
class TestPasswordReset:
    """Test cases for password reset functionality."""

    def test_password_reset_request(self, create_user):
        """Test requesting password reset."""
        user = create_user()
        client = APIClient()
        url = reverse('users-reset-password')
        data = {'email': user.email}
        response = client.post(url, data, format='json')
        assert response.status_code == 204


@pytest.mark.django_db
class TestUserActivation:
    """Test cases for user account activation."""

    def test_user_activation_request(self, create_user):
        """Test user activation process."""
        user = create_user()
        client = APIClient()
        url = reverse('users-activation')
        data = {
            'uid': 'test-uid',
            'token': 'test-token'
        }
        response = client.post(url, data, format='json')
        assert response.status_code in [200, 204, 400]
