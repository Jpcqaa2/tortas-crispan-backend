from django_filters import rest_framework as filters
from django_filters.rest_framework import DateFilter

from apps.sales.models.sales import Sales
from apps.purchases.models.purchases import Purchases


class SalesReportFilter(filters.FilterSet):
    start_date = DateFilter(field_name='sale_date', lookup_expr='gte')
    end_date = DateFilter(field_name='sale_date', lookup_expr='lte')

    class Meta:
        model = Sales
        fields=['sale_date']


class PurchaseReportFilter(filters.FilterSet):
    start_date = DateFilter(field_name='purchase_date', lookup_expr='gte')
    end_date = DateFilter(field_name='purchase_date', lookup_expr='lte')

    class Meta:
        model = Purchases
        fields=['purchase_date']