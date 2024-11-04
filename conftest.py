import pytest

from apps.users.models.users import User


@pytest.fixture
def user_created():
    return User.objects.create_superuser(username='admin', password='admin', email='admin@test.com')