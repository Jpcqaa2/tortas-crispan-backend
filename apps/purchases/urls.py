"""Users urls."""

# Django
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from apps.purchases import views

router = DefaultRouter()
router.register(r'purchases', views.PurchaseViewSet, basename='purchases')

urlpatterns = [
    path('', include(router.urls)),
]
