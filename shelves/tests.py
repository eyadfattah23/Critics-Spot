import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from shelves.models import Shelf, ShelfBook
from users.models import CustomUser
from books.models import Book, Author

@pytest.mark.django_db
def test_create_shelf():
    user = CustomUser.objects.create_user(
        username='shelfowner',
        email='owner@example.com',
        password='password123'
    )
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('user-shelves-list', args=[user.id])
    data = {
        'name': 'Test Shelf'
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 201
    assert Shelf.objects.filter(name='Test Shelf').exists()

@pytest.mark.django_db
def test_retrieve_shelf():
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
