"""Utils urls."""

from django.urls import path

from apps.utils.views import basics


urlpatterns = [
    path(r'basics/customers/', basics.CustomersList.as_view(), name="basics_customers"),
    path(r'basics/products/', basics.ProductsList.as_view(), name="basics_products"),
    path(r'basics/articles/', basics.ArticlesList.as_view(), name="basics_articles"),
    path(r'basics/suppliers/', basics.SuppliersList.as_view(), name="basics_suppliers"),
    path(r'basics/payment_methods/', basics.PaymentMethodList.as_view(), name="basics_payment_methods"),
    path(r'basics/measurement_units/', basics.MeasurementUnitList.as_view(), name="basics_measurement_unit"),
    path(r'basics/identification_types/', basics.IdentificationTypesList.as_view(), name="basics_identification_types"),
    path(r'basics/cities/', basics.CitiesList.as_view(), name="basics_cities"),
    path(r'basics/article_types/', basics.ArticleTypesList.as_view(), name="basics_article_types"),
    path(r'basics/categories/', basics.CategoryList.as_view(), name="basics_categories"),
]