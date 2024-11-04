# Django
from django.utils.decorators import method_decorator
from django.db import transaction

# Django REST Framework
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Swagger
from drf_yasg.utils import swagger_auto_schema

#Filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from apps.sales.models.customers import Customers
from apps.sales.serializers.customers import CustomersModelSerializer, UpdateAndCreateCustomersSerializer


@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    auto_schema=None
))
class CustomerViewSet(mixins.ListModelMixin, 
                      mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):

    """
    API of customers
    """

    queryset = Customers.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name', 'identification_number']

    def get_serializer_class(self):
        """Return serializer based on action."""
        if self.action in ['update', 'partial_update', 'create']:
            return UpdateAndCreateCustomersSerializer
        return CustomersModelSerializer

    def get_permissions(self):
        permissions = [IsAuthenticated]
        return [permission() for permission in permissions]

    def list(self, request, *args, **kwargs):
        """ List customers

            Allow you to list all customers
        """
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """ Get customer by ID

            Allow you to get customer by ID
        """
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={status.HTTP_201_CREATED: CustomersModelSerializer(many=False)})
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """ Create customer

            Allow you to create customer
        """
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        data = CustomersModelSerializer(instance=serializer.save()).data
        return Response(data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: CustomersModelSerializer(many=False)})
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        """ Update customer
        
            Allow you to update customer by ID
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        data = CustomersModelSerializer(instance=instance).data
        return Response(data=data, status=status.HTTP_200_OK)
    
    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
