import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from communities.models import Community, Post, Comment, Like
from users.models import CustomUser

@pytest.mark.django_db
def test_create_community():
    client = APIClient()
    user = CustomUser.objects.create_user(
        username='communityowner',
        email='owner@example.com',
        password='password123'
    )
    client.force_authenticate(user=user)
    url = reverse('community-list')
    data = {
        'name': 'Test Community',
        'description': 'A community for testing purposes'
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 201
    assert Community.objects.filter(name='Test Community').exists()

@pytest.mark.django_db
def test_retrieve_community():
    user = CustomUser.objects.create_user(
        username='communityowner',
        email='owner@example.com',
        password='password123'
    )
    community = Community.objects.create(
        name='Test Community',
        description='A community for testing purposes',
        owner=user
    )
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('community-detail', args=[community.id])
    response = client.get(url)
    assert response.status_code == 200
    assert response.data['name'] == 'Test Community'

@pytest.mark.django_db
def test_update_community():
    user = CustomUser.objects.create_user(
        username='communityowner',
        email='owner@example.com',
        password='password123'
    )
    community = Community.objects.create(
        name='Test Community',
        description='A community for testing purposes',
        owner=user
    )
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('community-detail', args=[community.id])
    data = {
        'description': 'Updated description'
    }
    response = client.patch(url, data, format='json')
    assert response.status_code == 200
    assert response.data['description'] == 'Updated description'

@pytest.mark.django_db
def test_delete_community():
    user = CustomUser.objects.create_user(
        username='communityowner',
        email='owner@example.com',
        password='password123'
    )
    community = Community.objects.create(
        name='Test Community',
        description='A community for testing purposes',
        owner=user
    )
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('community-detail', args=[community.id])
    response = client.delete(url)
    assert response.status_code == 204
    assert not Community.objects.filter(name='Test Community').exists()


@pytest.mark.django_db
def test_create_post():
    user = CustomUser.objects.create_user(
        username='postowner',
        email='owner@example.com',
        password='password123'
    )
    community = Community.objects.create(
        name='Test Community',
        description='A community for testing purposes',
        owner=user
    )
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('community-posts-list', args=[community.id])
    data = {
        'content': 'This is a test post'
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 201
    assert Post.objects.filter(content='This is a test post').exists()

@pytest.mark.django_db
def test_retrieve_post():
    user = CustomUser.objects.create_user(
        username='postowner',
        email='owner@example.com',
        password='password123'
    )
    community = Community.objects.create(
        name='Test Community',
        description='A community for testing purposes',
        owner=user
    )
    post = Post.objects.create(
        content='This is a test post',
        user=user,
        community=community
    )
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('community-posts-detail', args=[community.id, post.id])
    response = client.get(url)
    assert response.status_code == 200
    assert response.data['content'] == 'This is a test post'

@pytest.mark.django_db
def test_update_post():
    user = CustomUser.objects.create_user(
        username='postowner',
        email='owner@example.com',
        password='password123'
    )
    community = Community.objects.create(
        name='Test Community',
        description='A community for testing purposes',
        owner=user
    )
    post = Post.objects.create(
        content='This is a test post',
        user=user,
        community=community
    )
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('community-posts-detail', args=[community.id, post.id])
    data = {
        'content': 'Updated test post'
    }
    response = client.patch(url, data, format='json')
    assert response.status_code == 200
    assert response.data['content'] == 'Updated test post'

@pytest.mark.django_db
def test_delete_post():
    user = CustomUser.objects.create_user(
        username='postowner',
        email='owner@example.com',
        password='password123'
    )
    community = Community.objects.create(
        name='Test Community',
        description='A community for testing purposes',
        owner=user
    )
    post = Post.objects.create(
        content='This is a test post',
        user=user,
        community=community
    )
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('community-posts-detail', args=[community.id, post.id])
    response = client.delete(url)
    assert response.status_code == 204
    assert not Post.objects.filter(content='This is a test post').exists()
