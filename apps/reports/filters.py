from apps.sales.models.sales import Sales
from django_filters import rest_framework as filters
from django_filters.rest_framework import DateFilter


class SalesReportFilter(filters.FilterSet):
    start_date = DateFilter(field_name='created', lookup_expr='gte')
    end_date = DateFilter(field_name='created', lookup_expr='lte')

    class Meta:
        model = Sales
        fields=['created']