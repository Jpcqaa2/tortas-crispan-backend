
# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.utils.constants import PaymentMethodChoices
from apps.utils.models.base import DateBaseModel


class Purchases(DateBaseModel):

    supplier = models.ForeignKey('purchases.Suppliers', on_delete=models.CASCADE)
    payment_method = models.CharField(
        max_length=1, 
        choices=PaymentMethodChoices.choices, 
        default=PaymentMethodChoices.EFECTIVO
    )
    description = models.CharField(max_length=150, null=True)
    purchase_date = models.DateField()
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    total = models.BigIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "{} {}".format(self.supplier, self.total)

    class Meta(DateBaseModel.Meta):
        db_table = 'purchases'
        managed = True
        verbose_name = 'purchases'
        verbose_name_plural = 'purchases'
