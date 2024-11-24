"""Users urls."""

# Django
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from apps.reports import views

router = DefaultRouter()
router.register(r'reports', views.SalesReportsViewset, basename='reports')

urlpatterns = [
    path('', include(router.urls)),
]
