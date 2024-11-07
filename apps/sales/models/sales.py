# apps/sales/models/sales.py
from django.db import models

# Utils
from apps.utils.models.base import DateBaseModel
from apps.utils.constants import PaymentMethodChoices


class Sales(DateBaseModel):
    """
    Modelo para almacenar información sobre ventas realizadas.
    """
    customer = models.ForeignKey('sales.Customers', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    payment_method = models.CharField(
        max_length=1,
        choices=PaymentMethodChoices.choices,
        default=PaymentMethodChoices.EFECTIVO
    )
    sale_status = models.ForeignKey('sales.SalesStatus', on_delete=models.PROTECT)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Venta #{self.id} - Cliente: {self.customer.name} - Total: ${self.total}"

    class Meta(DateBaseModel.Meta):
        db_table = 'sales'
        managed = True
        verbose_name = 'sale'
        verbose_name_plural = 'sales'
