from django.contrib import admin
from apps.sales.models.products import Products
from apps.sales.models.sales import Sales
from apps.sales.models.categories import Categories
from apps.sales.models.customers import Customers
from apps.sales.models.sales_status import SalesStatus
from apps.sales.models.sales_details import SalesDetails

# Registrar los modelos aquí
admin.site.register(Products)
admin.site.register(Sales)
admin.site.register(Categories)
admin.site.register(Customers)
admin.site.register(SalesStatus)
admin.site.register(SalesDetails)
