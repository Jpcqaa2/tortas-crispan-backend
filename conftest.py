import pytest

from django.core.management import call_command
from rest_framework.test import APIClient

from apps.users.models.users import User


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user_created():
    return User.objects.create_superuser(username='admin', password='admin', email='admin@test.com')


@pytest.fixture(scope='session', autouse=True)
def cargar_datos_bd(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'fixtures/departments.json')
        call_command('loaddata', 'fixtures/cities.json')
        call_command('loaddata', 'fixtures/groups.json')
        call_command('loaddata', 'fixtures/categories.json')
        call_command('loaddata', 'fixtures/customers.json')
        call_command('loaddata', 'fixtures/products.json')
        call_command('loaddata', 'fixtures/sales_status.json')
        call_command('loaddata', 'fixtures/article_types.json')
        call_command('loaddata', 'fixtures/articles.json')
        call_command('loaddata', 'fixtures/suppliers.json')