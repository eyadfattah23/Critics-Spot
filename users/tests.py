import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth.models import Permission
from users.models import CustomUser

@pytest.mark.django_db
def test_create_user():
    client = APIClient()
    url = reverse('user-list')
    data = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword123'
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 201
    assert CustomUser.objects.filter(username='testuser').exists()

@pytest.mark.django_db
def test_retrieve_user():
    user = CustomUser.objects.create_user(
        username='testuser',
        email='testuser@example.com',
        password='testpassword123'
    )
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('user-details', args=[user.id])
    response = client.get(url)
    assert response.status_code == 200
    assert response.data['username'] == 'testuser'

@pytest.mark.django_db
def test_update_user():
    user = CustomUser.objects.create_user(
        username='testuser',
        email='testuser@example.com',
        password='testpassword123'
    )
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('user-details', args=[user.id])
    data = {
        'first_name': 'UpdatedName'
    }
    response = client.patch(url, data, format='json')
    assert response.status_code == 200
    assert response.data['first_name'] == 'UpdatedName'

@pytest.mark.django_db
def test_delete_user():
    user = CustomUser.objects.create_user(
        username='testuser',
        email='testuser@example.com',
        password='testpassword123'
    )
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('user-details', args=[user.id])
    response = client.delete(url)
    assert response.status_code == 204
    assert not CustomUser.objects.filter(username='testuser').exists()
