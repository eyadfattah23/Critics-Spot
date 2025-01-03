import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth.models import Permission
from books.models import Book, Author, Genre
from users.models import CustomUser

@pytest.mark.django_db
def test_create_book():
    user = CustomUser.objects.create_user(
        username='bookowner',
        email='owner@example.com',
        password='password123'
    )
    # Assign necessary permissions to the user
    permissions = Permission.objects.filter(codename__in=['add_book', 'view_book', 'change_book', 'delete_book'])
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
    user = CustomUser.objects.create_user(
        username='bookowner',
        email='owner@example.com',
        password='password123'
    )
    # Assign necessary permissions to the user
    permissions = Permission.objects.filter(codename__in=['add_book', 'view_book', 'change_book', 'delete_book'])
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
    user = CustomUser.objects.create_user(
        username='bookowner',
        email='owner@example.com',
        password='password123'
    )
    # Assign necessary permissions to the user
    permissions = Permission.objects.filter(codename__in=['add_book', 'view_book', 'change_book', 'delete_book'])
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
    user = CustomUser.objects.create_user(
        username='bookowner',
        email='owner@example.com',
        password='password123'
    )
    # Assign necessary permissions to the user
    permissions = Permission.objects.filter(codename__in=['add_book', 'view_book', 'change_book', 'delete_book'])
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
