# Django rest framework
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from apps.purchases.models.articles import Articles
from apps.purchases.models.suppliers import Suppliers
from apps.sales.models.customers import Customers
from apps.sales.models.products import Products
from apps.utils.constants import MeasurementUnitChoices, PaymentMethodChoices
from apps.utils.filters import ArticlesBasicFilter, CustomersBasicFilter, ProductsBasicFilter, SuppliersBasicFilter
from apps.utils.serializers.globals import DataSerializer


class CustomersList(generics.ListAPIView):
    """ List Customers

    This API return information about all customer registrered in the system.

    You can filter o searh by all parameters described below:
    """
    queryset = Customers.objects.all()
    pagination_class = None
    serializer_class = DataSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['^id', 'name', 'identification_number', 'email']
    filterset_class = CustomersBasicFilter


class SuppliersList(generics.ListAPIView):
    """ List Suppliers

    This API return information about all suppliers registrered in the system.

    You can filter o searh by all parameters described below:
    """
    queryset = Suppliers.objects.all()
    pagination_class = None
    serializer_class = DataSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['^id', 'name', 'cell_phone', 'email']
    filterset_class = SuppliersBasicFilter


class ProductsList(generics.ListAPIView):
    """ List Products

    This API return information about all products registrered in the system.

    You can filter o searh by all parameters described below:
    """
    queryset = Products.objects.all()
    pagination_class = None
    serializer_class = DataSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['^id', 'name', 'description']
    filterset_class = ProductsBasicFilter


class ArticlesList(generics.ListAPIView):
    """ List Articles

    This API return information about all articles registrered in the system.

    You can filter o searh by all parameters described below:
    """
    queryset = Articles.objects.all()
    pagination_class = None
    serializer_class = DataSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['^id', 'name', 'presentation']
    filterset_class = ArticlesBasicFilter


class PaymentMethodList(generics.ListAPIView):
    """ List Payment Methods

    This API return information about all payment methods configured in the system.

    You can filter o searh by all parameters described below:
    """
    queryset = None
    pagination_class = None
    serializer_class = DataSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        data = [{'value': value, 'label': label} for value, label in PaymentMethodChoices.choices]
        return Response(data)
    

class MeasurementUnitList(generics.ListAPIView):
    """ List Measurement Unit

    This API return information about all measurement units configured in the system.

    You can filter o searh by all parameters described below:
    """
    queryset = None
    pagination_class = None
    serializer_class = DataSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        data = [{'value': value, 'label': label} for value, label in MeasurementUnitChoices.choices]
        return Response(data)