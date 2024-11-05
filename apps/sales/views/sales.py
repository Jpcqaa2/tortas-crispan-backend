# Django
from django.utils.decorators import method_decorator
from django.db import transaction

# Django REST Framework
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action  


# Swagger
from drf_yasg.utils import swagger_auto_schema

# Filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

# Models y Serializers
from apps.sales.models import Sales, SalesStatus
from apps.sales.serializers.sales import SalesModelSerializer, UpdateAndCreateSalesSerializer


@method_decorator(name='partial_update', decorator=swagger_auto_schema(auto_schema=None))
class SalesViewSet(mixins.ListModelMixin, 
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """
    API for managing sales.
    """

    queryset = Sales.objects.exclude(sale_status_id=7)
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['customer__name', 'user__username']
    
    def get_serializer_class(self):
        """Return the serializer based on the action."""
        if self.action in ['create', 'update', 'partial_update']:
            return UpdateAndCreateSalesSerializer
        return SalesModelSerializer

    def get_permissions(self):
        """Set permissions for the view."""
        permissions = [IsAuthenticated]
        return [permission() for permission in permissions]

    @swagger_auto_schema(
        responses={status.HTTP_201_CREATED: SalesModelSerializer(many=False)}
    )
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """Create a sale with sale details."""
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        sale_data = SalesModelSerializer(instance=serializer.save()).data
        return Response(sale_data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: SalesModelSerializer(many=False)}
    )
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        """Update a sale and its details by ID."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        updated_instance = serializer.save()
        sale_data = SalesModelSerializer(instance=updated_instance).data
        return Response(data=sale_data, status=status.HTTP_200_OK)

    @transaction.atomic
    def perform_destroy(self, instance):
        """Soft delete the sale record."""
        canceled_status = SalesStatus.objects.get(name='CANCELADO')
        instance.sale_status = canceled_status
        instance.is_active = False
        instance.save()

    @action(detail=False, methods=['get'])
    def all_sales(self, request):
        """Retrieve all sales, including inactive ones."""
        include_inactive = request.query_params.get('include_inactive', 'false').lower() == 'true'
        
        if include_inactive:
            queryset = Sales.objects.all()  # Todas las ventas, activas e inactivas
        else:
            queryset = Sales.objects.exclude(sale_status_id=7)  # Solo las ventas activas
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)