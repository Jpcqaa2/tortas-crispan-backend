"""Users urls."""

# Django
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from apps.sales import views

router = DefaultRouter()
router.register(r'customers', views.CustomerViewSet, basename='customers')

urlpatterns = [
    path('', include(router.urls)),
]
