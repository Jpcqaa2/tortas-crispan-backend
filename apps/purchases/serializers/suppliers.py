
# Django REST Framework
from rest_framework import serializers

# Models
from apps.purchases.models.suppliers import Suppliers

# Serializers
from apps.utils.serializers.globals import DataSerializer


class SuppliersModelSerializer(serializers.ModelSerializer):
    city = DataSerializer()

    class Meta:
        model = Suppliers
        fields = '__all__'