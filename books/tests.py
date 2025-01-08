#!/usr/bin/python3
"""Test creating a new book."""
import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth.models import Permission
from books.models import Book, Author, Genre
from users.models import CustomUser


@pytest.mark.django_db
def test_create_book():
    """Test creating a new book."""
    user = CustomUser.objects.create_user(
        username='bookowner',
        email='owner@example.com',
        password='password123'
    )
    # Assign necessary permissions to the user
    permissions = Permission.objects.filter(
        codename__in=[
            'add_book',
            'view_book',
            'change_book',
            'delete_book'])
    user.user_permissions.add(*permissions)

    author = Author.objects.create(name='Test Author', birth_date='1980-01-01')
    genre = Genre.objects.create(name='Test Genre')

    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('book-list')
    data = {
        'title': 'Test Book',
        'author': author.id,
        'genres': [genre.id],
        'publication_date': '2023-01-01',
        'pages': 100
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 201
    assert Book.objects.filter(title='Test Book').exists()


@pytest.mark.django_db
def test_retrieve_book():
    """Test retrieving a book."""
    user = CustomUser.objects.create_user(
        username='bookowner',
        email='owner@example.com',
        password='password123'
    )
    # Assign necessary permissions to the user
    permissions = Permission.objects.filter(
        codename__in=[
            'add_book',
            'view_book',
            'change_book',
            'delete_book'])
    user.user_permissions.add(*permissions)

    author = Author.objects.create(name='Test Author', birth_date='1980-01-01')
    genre = Genre.objects.create(name='Test Genre')
    book = Book.objects.create(
        title='Test Book',
        author=author,
        publication_date='2023-01-01',
        pages=100
    )
    book.genres.add(genre)

    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('book-details', args=[book.id])
    response = client.get(url)
    assert response.status_code == 200
    assert response.data['title'] == 'Test Book'


@pytest.mark.django_db
def test_update_book():
    """Test updating a book."""
    user = CustomUser.objects.create_user(
        username='bookowner',
        email='owner@example.com',
        password='password123'
    )
    # Assign necessary permissions to the user
    permissions = Permission.objects.filter(
        codename__in=[
            'add_book',
            'view_book',
            'change_book',
            'delete_book'])
    user.user_permissions.add(*permissions)

    author = Author.objects.create(name='Test Author', birth_date='1980-01-01')
    genre = Genre.objects.create(name='Test Genre')
    book = Book.objects.create(
        title='Test Book',
        author=author,
        publication_date='2023-01-01',
        pages=100
    )
    book.genres.add(genre)

    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('book-details', args=[book.id])
    data = {
        'title': 'Updated Test Book'
    }
    response = client.patch(url, data, format='json')
    assert response.status_code == 200
    assert response.data['title'] == 'Updated Test Book'


@pytest.mark.django_db
def test_delete_book():
    """Test deleting a book."""
    user = CustomUser.objects.create_user(
        username='bookowner',
        email='owner@example.com',
        password='password123'
    )
    # Assign necessary permissions to the user
    permissions = Permission.objects.filter(
        codename__in=[
            'add_book',
            'view_book',
            'change_book',
            'delete_book'])
    user.user_permissions.add(*permissions)

    author = Author.objects.create(name='Test Author', birth_date='1980-01-01')
    genre = Genre.objects.create(name='Test Genre')
    book = Book.objects.create(
        title='Test Book',
        author=author,
        publication_date='2023-01-01',
        pages=100
    )
    book.genres.add(genre)

    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('book-details', args=[book.id])
    response = client.delete(url)
    assert response.status_code == 204
    assert not Book.objects.filter(title='Test Book').exists()


@pytest.mark.django_db
def test_create_author():
    """Test creating a new author."""
    user = CustomUser.objects.create_user(
        username='authorowner',
        email='owner@example.com',
        password='password123'
    )
    # Assign necessary permissions to the user
    permissions = Permission.objects.filter(
        codename__in=[
            'add_author',
            'view_author',
            'change_author',
            'delete_author'])
    user.user_permissions.add(*permissions)

    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('author-list')
    data = {
        'name': 'Test Author',
        'birth_date': '1980-01-01'
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 201
    assert Author.objects.filter(name='Test Author').exists()


@pytest.mark.django_db
def test_retrieve_author():
    """Test retrieving an author."""
    user = CustomUser.objects.create_user(
        username='authorowner',
        email='owner@example.com',
        password='password123'
    )
    # Assign necessary permissions to the user
    permissions = Permission.objects.filter(
        codename__in=[
            'add_author',
            'view_author',
            'change_author',
            'delete_author'])
    user.user_permissions.add(*permissions)

    author = Author.objects.create(name='Test Author', birth_date='1980-01-01')

    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('author-details', args=[author.id])
    response = client.get(url)
    assert response.status_code == 200
    assert response.data['name'] == 'Test Author'


@pytest.mark.django_db
def test_update_author():
    """Test updating an author."""
    user = CustomUser.objects.create_user(
        username='authorowner',
        email='owner@example.com',
        password='password123'
    )
    # Assign necessary permissions to the user
    permissions = Permission.objects.filter(
        codename__in=[
            'add_author',
            'view_author',
            'change_author',
            'delete_author'])
    user.user_permissions.add(*permissions)

    author = Author.objects.create(name='Test Author', birth_date='1980-01-01')

    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('author-details', args=[author.id])
    data = {
        'name': 'Updated Test Author'
    }
    response = client.patch(url, data, format='json')
    assert response.status_code == 200
    assert response.data['name'] == 'Updated Test Author'


@pytest.mark.django_db
def test_delete_author():
    """Test deleting an author."""
    user = CustomUser.objects.create_user(
        username='authorowner',
        email='owner@example.com',
        password='password123'
    )
    # Assign necessary permissions to the user
    permissions = Permission.objects.filter(
        codename__in=[
            'add_author',
            'view_author',
            'change_author',
            'delete_author'])
    user.user_permissions.add(*permissions)

    author = Author.objects.create(name='Test Author', birth_date='1980-01-01')

    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('author-details', args=[author.id])
    response = client.delete(url)
    assert response.status_code == 204
    assert not Author.objects.filter(name='Test Author').exists()


@pytest.mark.django_db
def test_create_genre():
    """Test creating a new genre."""
    user = CustomUser.objects.create_user(
        username='genreowner',
        email='owner@example.com',
        password='password123'
    )
    # Assign necessary permissions to the user
    permissions = Permission.objects.filter(
        codename__in=[
            'add_genre',
            'view_genre',
            'change_genre',
            'delete_genre'])
    user.user_permissions.add(*permissions)

    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('genre-list')
    data = {
        'name': 'Test Genre'
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 201
    assert Genre.objects.filter(name='Test Genre').exists()


@pytest.mark.django_db
def test_retrieve_genre():
    """Test retrieving a genre."""
    user = CustomUser.objects.create_user(
        username='genreowner',
        email='owner@example.com',
        password='password123'
    )
    # Assign necessary permissions to the user
    permissions = Permission.objects.filter(
        codename__in=[
            'add_genre',
            'view_genre',
            'change_genre',
            'delete_genre'])
    user.user_permissions.add(*permissions)

    genre = Genre.objects.create(name='Test Genre')

    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('genre-details', args=[genre.id])
    response = client.get(url)
    assert response.status_code == 200
    assert response.data['name'] == 'Test Genre'


@pytest.mark.django_db
def test_update_genre():
    """Test updating a genre."""
    user = CustomUser.objects.create_user(
        username='genreowner',
        email='owner@example.com',
        password='password123'
    )
    # Assign necessary permissions to the user
    permissions = Permission.objects.filter(
        codename__in=[
            'add_genre',
            'view_genre',
            'change_genre',
            'delete_genre'])
    user.user_permissions.add(*permissions)

    genre = Genre.objects.create(name='Test Genre')

    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('genre-details', args=[genre.id])
    data = {
        'name': 'Updated Test Genre'
    }
    response = client.patch(url, data, format='json')
    assert response.status_code == 200
    assert response.data['name'] == 'Updated Test Genre'


@pytest.mark.django_db
def test_delete_genre():
    """Test deleting a genre."""
    user = CustomUser.objects.create_user(
        username='genreowner',
        email='owner@example.com',
        password='password123'
    )
    # Assign necessary permissions to the user
    permissions = Permission.objects.filter(
        codename__in=[
            'add_genre',
            'view_genre',
            'change_genre',
            'delete_genre'])
    user.user_permissions.add(*permissions)

    genre = Genre.objects.create(name='Test Genre')

    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('genre-details', args=[genre.id])
    response = client.delete(url)
    assert response.status_code == 204
    assert not Genre.objects.filter(name='Test Genre').exists()
