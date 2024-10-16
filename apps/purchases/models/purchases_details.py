
# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.utils.models.base import DateBaseModel


class MeasurmentUnitChoices(models.TextChoices):
    GRAMO = '1',_('Gramos')
    KILO_GRAMO = '2',_('Kilo Gramo')
    LIBRA = '3',_('Libra')
    LITRO = '4',_('Litro')


class PurchasesDetails(DateBaseModel):

    purchase = models.ForeignKey('purchases.Purchases', on_delete=models.CASCADE)
    article = models.ForeignKey('purchases.Articles', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    unit_price = models.BigIntegerField(default=0)
    measurment_unit = models.CharField(max_length=1, choices=MeasurmentUnitChoices.choices)
    subtotal = models.BigIntegerField(default=0)
  
    def __str__(self):
        return "{} {}".format(self.purchase, self.article)

    class Meta(DateBaseModel.Meta):
        db_table = 'purchases_details'
        managed = True
        verbose_name = 'purchases details'
        verbose_name_plural = 'purchases details'
