# Django rest framework
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from apps.purchases.models.article_types import ArticleTypes
from apps.purchases.models.articles import Articles
from apps.purchases.models.suppliers import Suppliers
from apps.sales.models.categories import Categories
from apps.sales.models.customers import Customers, IdentificationTypeChoices
from apps.sales.models.products import Products
from apps.utils.constants import MeasurementUnitChoices, PaymentMethodChoices
from apps.utils.filters import ArticlesBasicFilter, CustomersBasicFilter, ProductsBasicFilter, SuppliersBasicFilter
from apps.utils.models.cities import City
from apps.utils.serializers.globals import DataSerializer


class CustomersList(generics.ListAPIView):
    """ List Customers

    This API return information about all customer registrered in the system.

    You can filter o searh by all parameters described below:
    """
    queryset = Customers.objects.filter(is_active=True)
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
    queryset = Suppliers.objects.filter(is_active=True)
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
    queryset = Products.objects.filter(is_active=True)
    pagination_class = None
    serializer_class = DataSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['^id', 'name', 'description']
    filterset_class = ProductsBasicFilter


class CategoryList(generics.ListAPIView):
    """ List Categories

    This API return information about all categories registrered in the system.

    You can filter o searh by all parameters described below:
    """
    queryset = Categories.objects.all()
    pagination_class = None
    serializer_class = DataSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['^id', 'name']


class ArticlesList(generics.ListAPIView):
    """ List Articles

    This API return information about all articles registrered in the system.

    You can filter o searh by all parameters described below:
    """
    queryset = Articles.objects.filter(is_active=True)
    pagination_class = None
    serializer_class = DataSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['^id', 'name', 'presentation']
    filterset_class = ArticlesBasicFilter


class ArticleTypesList(generics.ListAPIView):
    """ List Article Types

    This API return information about all article types registrered in the system.

    You can filter o searh by all parameters described below:
    """
    queryset = ArticleTypes.objects.all()
    pagination_class = None
    serializer_class = DataSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['^id', 'name']


class CitiesList(generics.ListAPIView):
    """ List Cities

    This API return information about all cities registrered in the system.

    You can filter o searh by all parameters described below:
    """
    queryset = City.objects.all()
    pagination_class = None
    serializer_class = DataSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['^id', 'name']



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
    

class IdentificationTypesList(generics.ListAPIView):
    """ List Identification Types

    This API return information about all identification types configured in the system.

    You can filter o searh by all parameters described below:
    """
    queryset = None
    pagination_class = None
    serializer_class = DataSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        data = [{'value': value, 'label': label} for value, label in IdentificationTypeChoices.choices]
        return Response(data)
    