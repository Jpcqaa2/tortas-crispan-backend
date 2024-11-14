
from rest_framework import serializers
from apps.sales.models import Sales, SalesDetails
from apps.utils.serializers.globals import DataChoiceSerializer
from apps.users.serializers.users import UserModelSerializer


class SalesDetailsModelSerializer(serializers.ModelSerializer):
    subtotal = serializers.ReadOnlyField()

    class Meta:
        model = SalesDetails
        exclude = ('sale',)


class SalesModelSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(read_only=True)
    payment_method = DataChoiceSerializer()
    user = UserModelSerializer()
    sale_details = serializers.SerializerMethodField()

    class Meta:
        model = Sales
        fields = '__all__'

    def get_sale_details(self, obj):
        """Fetch related sale details."""
        details = SalesDetails.objects.filter(sale=obj)
        return SalesDetailsModelSerializer(details, many=True).data


class UpdateAndCreateSalesDetailsSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating SalesDetails records."""
    
    class Meta:
        model = SalesDetails
        exclude = ('sale',)




class UpdateAndCreateSalesSerializer(serializers.ModelSerializer):
    sale_details = UpdateAndCreateSalesDetailsSerializer(many=True, required=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Sales
        fields = '__all__'

    def create(self, validated_data):
        return self._create_or_update_sales(validated_data)

    def update(self, instance, validated_data):
        return self._create_or_update_sales(validated_data, instance)

    def _create_or_update_sales(self, validated_data, instance=None):
        sale_details_data = validated_data.pop('sale_details')
        
        if instance:
            sale = super().update(instance, validated_data)
        else:
            sale = super().create(validated_data)
        
        total = self._create_sale_details(sale, sale_details_data)
        sale.total = total
        sale.save()
        return sale

    def _create_sale_details(self, sale, sale_details_data):
        """Create SalesDetails records and calculate total."""
        SalesDetails.objects.filter(sale=sale).delete()
        total = 0
        for detail_data in sale_details_data:
            detail_data['sale'] = sale
            detail_data['subtotal'] = detail_data['quantity'] * detail_data['unit_value'] 
            sale_detail = SalesDetails.objects.create(**detail_data)
            total += sale_detail.subtotal
        return total
