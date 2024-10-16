# Django
from django.utils.decorators import method_decorator
from django.db import transaction

# Django REST Framework
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

# Swagger
from drf_yasg.utils import swagger_auto_schema

#Filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from apps.purchases.filter import PurchasesFilter
from apps.purchases.models.purchases import Purchases
from apps.purchases.serializers.purchases import PurchasesModelSerializer, UpdateAndCreatePurchasesSerializer


@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    auto_schema=None
))
class PurchaseViewSet(mixins.ListModelMixin, 
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):

    """
    API of purchases
    """

    queryset = Purchases.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['supplier__name']
    filterset_class = PurchasesFilter

    def get_serializer_class(self):
        """Return serializer based on action."""
        if self.action in ['update', 'partial_update', 'create']:
            return UpdateAndCreatePurchasesSerializer
        return PurchasesModelSerializer

    def get_permissions(self):
        permissions = [IsAuthenticated]
        return [permission() for permission in permissions]

    def list(self, request, *args, **kwargs):
        """ List purchases

            Allow you to list all purchases
        """
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """ Get purchase by ID

            Allow you to get purchase by ID
        """
        return super().retrieve(request, *args, **kwargs)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """ Create purchase

            Allow you to create purchase
        """
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        data = PurchasesModelSerializer(instance=serializer.save()).data
        return Response(data, status=status.HTTP_201_CREATED)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        """ Update purchase
        
            Allow you to update purchase by ID
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
        data = PurchasesModelSerializer(instance=instance).data
        return Response(data=data, status=status.HTTP_200_OK)
    
    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()