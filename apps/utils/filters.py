from django_filters import rest_framework as filters

from apps.purchases.models.articles import Articles
from apps.purchases.models.suppliers import Suppliers
from apps.sales.models.customers import Customers
from apps.sales.models.products import Products


class CustomersBasicFilter(filters.FilterSet):
    identification_type = filters.CharFilter(field_name="identification_type")
    city = filters.CharFilter(field_name="city")

    class Meta:
        model = Customers
        fields = ['identification_type', 'city']


class SuppliersBasicFilter(filters.FilterSet):
    city = filters.CharFilter(field_name="city")

    class Meta:
        model = Suppliers
        fields = ['city']


class ProductsBasicFilter(filters.FilterSet):
    measurement_unit = filters.CharFilter(field_name="measurement_unit")
    category = filters.CharFilter(field_name="category")

    class Meta:
        model = Products
        fields = ['measurement_unit', 'category', 'featured_product']


class ArticlesBasicFilter(filters.FilterSet):
    article_type = filters.CharFilter(field_name="article_type")

    class Meta:
        model = Articles
        fields = ['article_type', 'is_disposible']