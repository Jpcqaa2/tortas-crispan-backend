# Django REST Framework
from rest_framework import serializers

# Models
from apps.purchases.models.purchases import Purchases

# Serializers
from apps.purchases.models.purchases_details import PurchasesDetails
from apps.purchases.serializers.suppliers import SuppliersModelSerializer
from apps.users.serializers.users import UserModelSerializer
from apps.utils.serializers.globals import DataChoiceSerializer, DataSerializer


class PurchasesDetailsModelSerializer(serializers.ModelSerializer):
    subtotal = serializers.ReadOnlyField()
    measurment_unit = DataChoiceSerializer()
    article = DataSerializer()

    class Meta:
        model = PurchasesDetails
        exclude = ('purchase',)


class PurchasesModelSerializer(serializers.ModelSerializer):
    supplier = SuppliersModelSerializer()
    payment_method = DataChoiceSerializer()
    user = UserModelSerializer()
    purchase_details = serializers.SerializerMethodField()

    class Meta:
        model = Purchases
        fields = '__all__'

    def get_purchase_details(self, obj):
        try:
            detail = PurchasesDetails.objects.filter(purchase=obj)
            return PurchasesDetailsModelSerializer(instance=detail, many=True).data
        except Exception:
            return None


class UpdateAndCreatePurchasesDetailsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchasesDetails
        exclude = ('purchase',)
  

class UpdateAndCreatePurchasesSerializer(serializers.ModelSerializer):
    purchase_details = UpdateAndCreatePurchasesDetailsModelSerializer(many=True, required=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
   
    class Meta:
        """Meta class."""
        model = Purchases
        fields = '__all__'

    def create(self, data):
        return self._update_or_update_purchase(data)
    
    def update(self, instance, data):
        return self._update_or_update_purchase(data, instance)
    
    def _update_or_update_purchase(self, data, instance=None):
        purchase_details = data.pop('purchase_details')
        if instance:
            purchase: Purchases = super().update(instance, data)
        else:
            purchase: Purchases = super().create(data)
        total_purchase = self._create_detail(purchase, purchase_details)
        purchase.total = total_purchase
        purchase.save()
        return purchase
    
    def _create_detail(self, purchase, purchase_details):
        PurchasesDetails.objects.filter(purchase=purchase).delete()
        total_purchase = 0
        for data_detail in purchase_details:
            data_detail['purchase'] = purchase
            data_detail['subtotal'] = (data_detail['quantity'] * data_detail['unit_price'])
            quotation_detail = PurchasesDetails.objects.create(**data_detail)
            total_purchase += quotation_detail.subtotal
        return total_purchase
        
