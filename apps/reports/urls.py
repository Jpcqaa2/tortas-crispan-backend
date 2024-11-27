"""Users urls."""

# Django
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from apps.reports import views

router = DefaultRouter()
router.register(r'reports/sales', views.SalesReportsViewset, basename='reports_sales')
router.register(r'reports/dashboard', views.DashboardReportsViewset, basename='reports_dashboard')

urlpatterns = [
    path('', include(router.urls)),
]
