"""Views user."""
# Django
from django.db import transaction
from django.contrib.auth import password_validation

# Django REST Framework
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response

# Models
from apps.users.models import User

# Serializers
from apps.users import serializers

#Filters
from django_filters.rest_framework import DjangoFilterBackend
from apps.users.filter import UsersFilter

# Swagger
from drf_yasg.utils import swagger_auto_schema


class UserViewSet(mixins.ListModelMixin, 
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):

    """
    API of users
    """

    queryset = User.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend]
    filterset_class = UsersFilter

    def get_serializer_class(self):
        if self.action == 'login':
            return serializers.CustomTokenObtainPairSerializer
        elif self.action == 'logout':
            return serializers.RefreshTokenSerializer
        if self.action in ['update', 'partial_update', 'create']:
            return serializers.UpdateAndCreateUserSerializer
        return serializers.UserModelSerializer

    def get_permissions(self):
        if self.action in ['login', 'password_reset', 'confirm_password_reset']:
            """ Cuando en 'Login' no se solicita al usuario estar autenticado """
            permissions = [AllowAny]
        else:
            permissions = [IsAuthenticated]
        return [permission() for permission in permissions]

    def list(self, request, *args, **kwargs):
        """ List users

            Allows you to list all users registered in the system
        """
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """ Consult user by ID

            Allow you to obtain information about user given their ID
        """
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        responses={status.HTTP_201_CREATED: serializers.UserModelSerializer(many=False)})
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """ Create users

            Allow you to crete users, who can log into the system.
        """
        serializer = self.get_serializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = serializers.UserModelSerializer(instance=user).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: serializers.UserModelSerializer(many=False)})
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        """ Update users
        
            Allows you to update a user based on their ID
        """
        user = self.get_object()
        serializer = self.get_serializer(
            instance=user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = serializers.UserModelSerializer(instance=user).data
        return Response(data=data, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        """Disable user."""
        instance.is_active = False
        instance.save()

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: serializers.UserLoginSerializer(many=False)})
    @action(detail=False, methods=['post'])
    def login(self, request):
        """ Authenticate users.

            - Allows you to authenticate a user by their email and password.
            - In case of success, return the user information and access token.
        """
        serializer = self.get_serializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = serializers.UserLoginSerializer(instance={'user': user, 'token': token}).data
        return Response(data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={status.HTTP_204_NO_CONTENT: ''})
    @action(detail=False, methods=['post'])
    def logout(self, request):
        """ Disable access tokens for user.

            - Allow you to disable user's access token.
            - This endpoint does not return information.
        """
        serializer = serializers.RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['GET'])
    def password_validations(self, request):
        """ List of enabled password validations. """
        data = password_validation.password_validators_help_texts()
        return Response(data, status=status.HTTP_200_OK)
       