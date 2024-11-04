import pytest
from django.urls import reverse

# DRF
from rest_framework import status

# Models
from apps.users.models.users import User


@pytest.mark.django_db
class TestAuthFlow:
    
    @pytest.fixture
    def user_data(self):
        return {
            "first_name": "Test",
            "last_name": "User",
            "identification_number": "23456789",
            "email": "testuser@example.com",
            "password": "SuperSecurePassword123",
            "groups": []
        }
    
    def __create_new_user(self, client, user_data):
        url = reverse('users:users-list') 
        return client.post(url, user_data, format='json')
    
    def __login_user(self, client, email, password):
        url_login = reverse('users:users-login')
        login_data = {
            "email": email,
            "password": password,
        }
        return client.post(url_login, login_data, format='json')
    
    def __logout_user(self, client, refresh):
        url_logout = reverse('users:users-logout')
        login_data = {
            "refresh": refresh,
        }
        return client.post(url_logout, login_data, format='json')

    def test_user_registration_not_login(self, client, user_data):
        """
        Test new user registration without using credentials.
        """
        response = self.__create_new_user(client, user_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_registration_login(self, client, user_data, user_created: User):
        """
        Test new user registration using credentials.
        """
        client.force_authenticate(user=user_created)
        response = self.__create_new_user(client, user_data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_user_login(self, client, user_data, user_created: User):
        """
        Test login with new registered user.
        """
        client.force_authenticate(user=user_created)
        self.__create_new_user(client, user_data)

        response = self.__login_user(client, user_data['email'], user_data['password'])
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data['token']
        assert 'refresh' in response.data['token']

    def test_user_logout(self, client, user_data, user_created: User):
        """
        Test logout with new registered user.
        """
        client.force_authenticate(user=user_created)
        self.__create_new_user(client, user_data)

        response = self.__login_user(client, user_data['email'], user_data['password'])
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data['token']
        assert 'refresh' in response.data['token']

        response = self.__logout_user(client, response.data['token']['refresh'])
        assert response.status_code == status.HTTP_204_NO_CONTENT
