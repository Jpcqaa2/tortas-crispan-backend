# Django REST Framework
from rest_framework import serializers

from apps.sales.models.products import Products
from apps.utils.serializers.globals import DataChoiceSerializer, DataSerializer


class ProductsModelSerializer(serializers.ModelSerializer):
    measurement_unit = DataChoiceSerializer()
    category = DataSerializer()

    class Meta:
        model = Products
        fields = '__all__'


class UpdateAndCreateProductsSerializer(serializers.ModelSerializer):
   
    class Meta:
        """Meta class."""
        model = Products
        fields = '__all__'

    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)