import pytest
import os
import django
import sys

from django.contrib.auth import get_user_model

sys.path.insert(0, os.path.abspath('.'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barter_platform.settings')
django.setup()

User = get_user_model()

@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='12345')

@pytest.fixture
def user1(db):
    return User.objects.create_user(username='user1', password='testpass123')

@pytest.fixture
def user2(db):
    return User.objects.create_user(username='user2', password='testpass123')

@pytest.fixture
def ad1(db, user1):
    from ads.models import Ad
    return Ad.objects.create(
        user=user1,
        title='Test Ad 1',
        description='Description 1',
        category='electronics',
        condition='new'
    )

@pytest.fixture
def ad2(db, user2):
    from ads.models import Ad
    return Ad.objects.create(
        user=user2,
        title='Test Ad 2',
        description='Description 2',
        category='books',
        condition='used'
    )

@pytest.fixture
def client_logged_in(client, user1):
    client.force_login(user1)
    return client
