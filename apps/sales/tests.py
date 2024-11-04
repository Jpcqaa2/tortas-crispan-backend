import pytest
from django.urls import reverse

# DRF
from rest_framework.test import APIClient
from rest_framework import status

from apps.users.models.users import User


@pytest.mark.django_db
class TestCustomers:

    @pytest.fixture
    def client(self):
        return APIClient()
    
    def test_get_customers(self, client: APIClient, user_created: User):
        client.force_authenticate(user=user_created)
        url = reverse('sales:customers-list') 
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_create_products(self, client: APIClient, user_created: User):
        client.force_authenticate(user=user_created)
        data = {
            'name': 'PRUEBAS',
            'price': 30000,
            'category': 1,
            'measurement_unit': 1,
        }
        url = reverse('sales:products-list')
        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED

    def test_update_products(self, client: APIClient, user_created: User):
        client.force_authenticate(user=user_created)
        data = {
            'name': 'PRUEBAS',
            'price': 30000,
            'category': 1,
        }
        url = reverse('sales:products-list')
        response_created = client.post(url, data, format='json')
        data = {'name': 'PRUEBAS EDITADO'}
        url_update = url+str(response_created.data['id'])+'/'
        response = client.patch(url_update, data, format='json')
        assert response.status_code == status.HTTP_200_OK and response.data.get('name') == 'PRUEBAS EDITADO'

    def test_delete_products(self, client: APIClient, user_created: User):
        client.force_authenticate(user=user_created)
        data = {
            'name': 'PRUEBAS',
            'price': 30000,
            'category': 1,
        }
        url = reverse('sales:products-list')
        response_created = client.post(url, data, format='json')
        url_update = url+str(response_created.data['id'])+'/'
        response = client.delete(url_update, format='json')
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_get_products(self, client: APIClient, user_created: User):
        client.force_authenticate(user=user_created)
        url = reverse('sales:products-list') 
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK