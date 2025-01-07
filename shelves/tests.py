#!/usr/bin/python3
"""
Tests for the shelves app.
"""
import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth.models import Permission
from shelves.models import Shelf, ShelfBook
from users.models import CustomUser
from books.models import Book, Author


@pytest.mark.django_db
def test_create_shelf():
    """
    Test creating a shelf.
    """
    user = CustomUser.objects.create_user(
        username='shelfowner',
        email='owner@example.com',
        password='password123'
    )
    # Assign necessary permissions to the user
    permissions = Permission.objects.filter(codename__in=['add_shelf', 'view_shelf', 'change_shelf', 'delete_shelf'])
    user.user_permissions.add(*permissions)

    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('user-shelves-list', args=[user.id])
    data = {
        'name': 'Test Shelf'
    }
    response = client.post(url, data, format='json')

    # Check if the user has the correct permissions
    user_permissions = user.get_all_permissions()
    print("User Permissions:", user_permissions)
    print("Response Data:", response.data)

    assert response.status_code == 201
    assert Shelf.objects.filter(name='Test Shelf').exists()


@pytest.mark.django_db
def test_retrieve_shelf():
    """
    Test retrieving a shelf.
    """
    user = CustomUser.objects.create_user(
        username='shelfowner',
        email='owner@example.com',
        password='password123'
    )
    shelf = Shelf.objects.create(
        name='Test Shelf',
        user=user
    )
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('shelf-detail', args=[shelf.id])
    response = client.get(url)
    assert response.status_code == 200
    assert response.data['name'] == 'Test Shelf'


@pytest.mark.django_db
def test_update_shelf():
    """
    Test updating a shelf.
    """
    user = CustomUser.objects.create_user(
        username='shelfowner',
        email='owner@example.com',
        password='password123'
    )
    shelf = Shelf.objects.create(
        name='Test Shelf',
        user=user
    )
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('shelf-detail', args=[shelf.id])
    data = {
        'name': 'Updated Test Shelf'
    }
    response = client.patch(url, data, format='json')
    assert response.status_code == 200
    assert response.data['name'] == 'Updated Test Shelf'


@pytest.mark.django_db
def test_delete_shelf():
    """
    Test deleting a shelf.
    """
    user = CustomUser.objects.create_user(
        username='shelfowner',
        email='owner@example.com',
        password='password123'
    )
    shelf = Shelf.objects.create(
        name='Test Shelf',
        user=user
    )
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('shelf-detail', args=[shelf.id])
    response = client.delete(url)
    assert response.status_code == 204
    assert not Shelf.objects.filter(name='Test Shelf').exists()


@pytest.mark.django_db
def test_add_book_to_shelf():
    """
    Test adding a book to a shelf.
    """
    user = CustomUser.objects.create_user(
        username='shelfowner',
        email='owner@example.com',
        password='password123'
    )
    author = Author.objects.create(name='Test Author', birth_date='1980-01-01')
    book = Book.objects.create(
        title='Test Book',
        author=author,
        publication_date='2023-01-01',
        pages=100
    )
    shelf = Shelf.objects.create(
        name='Test Shelf',
        user=user
    )
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('book-to-shelf', args=[shelf.id])
    data = {
        'book': book.id,
        'current_page': 50
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 201
    assert ShelfBook.objects.filter(shelf=shelf, book=book).exists()


@pytest.mark.django_db
def test_retrieve_books_from_shelf():
    """
    Test retrieving books from a shelf.
    """
    user = CustomUser.objects.create_user(
        username='shelfowner',
        email='owner@example.com',
        password='password123'
    )
    author = Author.objects.create(name='Test Author', birth_date='1980-01-01')
    book = Book.objects.create(
        title='Test Book',
        author=author,
        publication_date='2023-01-01',
        pages=100
    )
    shelf = Shelf.objects.create(
        name='Test Shelf',
        user=user
    )
    ShelfBook.objects.create(shelf=shelf, book=book, current_page=50)
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('shelf-detail', args=[shelf.id])
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data['books']) == 1
    assert response.data['books'][0]['title'] == 'Test Book'


@pytest.mark.django_db
def test_update_book_in_shelf():
    """
    Test updating a book in a shelf.
    """
    user = CustomUser.objects.create_user(
        username='shelfowner',
        email='owner@example.com',
        password='password123'
    )
    author = Author.objects.create(name='Test Author', birth_date='1980-01-01')
    book = Book.objects.create(
        title='Test Book',
        author=author,
        publication_date='2023-01-01',
        pages=100
    )
    shelf = Shelf.objects.create(
        name='Test Shelf',
        user=user
    )
    shelf_book = ShelfBook.objects.create(shelf=shelf, book=book, current_page=50)
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('book-to-shelf', args=[shelf.id, book.id])
    data = {
        'current_page': 100
    }
    response = client.patch(url, data, format='json')
    assert response.status_code == 200
    assert response.data['current_page'] == 100


@pytest.mark.django_db
def test_remove_book_from_shelf():
    """
    Test removing a book from a shelf.
    """
    user = CustomUser.objects.create_user(
        username='shelfowner',
        email='owner@example.com',
        password='password123'
    )
    author = Author.objects.create(name='Test Author', birth_date='1980-01-01')
    book = Book.objects.create(
        title='Test Book',
        author=author,
        publication_date='2023-01-01',
        pages=100
    )
    shelf = Shelf.objects.create(
        name='Test Shelf',
        user=user
    )
    shelf_book = ShelfBook.objects.create(shelf=shelf, book=book, current_page=50)
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('book-to-shelf', args=[shelf.id, book.id])
    response = client.delete(url)
    assert response.status_code == 204
    assert not ShelfBook.objects.filter(shelf=shelf, book=book).exists()


@pytest.mark.django_db
def test_retrieve_all_shelves_for_user():
    """
    Test retrieving all shelves for a user.
    """
    user = CustomUser.objects.create_user(
        username='shelfowner',
        email='owner@example.com',
        password='password123'
    )
    Shelf.objects.create(name='Test Shelf 1', user=user)
    Shelf.objects.create(name='Test Shelf 2', user=user)

    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('user-shelves-list', args=[user.id])
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 2
    assert response.data[0]['name'] == 'Test Shelf 1'
    assert response.data[1]['name'] == 'Test Shelf 2'


@pytest.mark.django_db
def test_unauthorized_user_cannot_access_or_modify_shelves():
    """
    Test that an unauthorized user cannot access or modify shelves.
    """
    user = CustomUser.objects.create_user(
        username='shelfowner',
        email='owner@example.com',
        password='password123'
    )
    unauthorized_user = CustomUser.objects.create_user(
        username='unauthorized',
        email='unauthorized@example.com',
        password='password123'
    )
    shelf = Shelf.objects.create(name='Test Shelf', user=user)

    client = APIClient()
    client.force_authenticate(user=unauthorized_user)

    # Test retrieval
    url = reverse('shelf-detail', args=[shelf.id])
    response = client.get(url)
    assert response.status_code == 403

    # Test update
    data = {'name': 'Updated Test Shelf'}
    response = client.patch(url, data, format='json')
    assert response.status_code == 403

    # Test deletion
    response = client.delete(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_pagination_for_shelf_books():
    """
    Test pagination for books on a shelf.
    """
    user = CustomUser.objects.create_user(
        username='shelfowner',
        email='owner@example.com',
        password='password123'
    )
    author = Author.objects.create(name='Test Author', birth_date='1980-01-01')
    shelf = Shelf.objects.create(name='Test Shelf', user=user)

    for i in range(15):
        book = Book.objects.create(title=f'Test Book {i}', author=author, publication_date='2023-01-01', pages=100)
        ShelfBook.objects.create(shelf=shelf, book=book, current_page=50)

    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('shelf-detail', args=[shelf.id])
    response = client.get(url, {'page': 1, 'page_size': 10})

    assert response.status_code == 200
    assert 'results' in response.data
    assert len(response.data['results']) == 10
    assert response.data['results'][0]['title'] == 'Test Book 0'
