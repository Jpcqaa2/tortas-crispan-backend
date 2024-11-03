# Django REST Framework
from rest_framework import serializers

from apps.sales.models.customers import Customers
from apps.utils.serializers.globals import DataChoiceSerializer, DataSerializer


class CustomersModelSerializer(serializers.ModelSerializer):
    subtotal = serializers.ReadOnlyField()
    identification_type = DataChoiceSerializer()
    city = DataSerializer()

    class Meta:
        model = Customers
        fields = '__all__'


class UpdateAndCreateCustomersSerializer(serializers.ModelSerializer):
   
    class Meta:
        """Meta class."""
        model = Customers
        fields = '__all__'

    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)