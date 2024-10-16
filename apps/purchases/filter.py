from django_filters.rest_framework import BaseInFilter, NumberFilter, DateFilter
from apps.purchases.models.purchases import Purchases
from django_filters import rest_framework as filters


class NumberInFilter(BaseInFilter, NumberFilter):
    pass


class PurchasesFilter(filters.FilterSet):

    created__gte = DateFilter(field_name='created', lookup_expr='date__gte')
    created__lte = DateFilter(field_name='created', lookup_expr='date__lte')
    supplier = NumberInFilter(field_name='supplier', lookup_expr='in')
    
    class Meta:
        model = Purchases
        fields = ['supplier', 'payment_method']