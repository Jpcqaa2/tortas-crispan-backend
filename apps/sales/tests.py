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
    
    def test_get_clients(self, client: APIClient, user_created: User):
        client.force_authenticate(user=user_created)
        url = reverse('sales:customers-list') 
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK