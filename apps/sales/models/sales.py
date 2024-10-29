# apps/sales/models/sales.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.utils.models.base import DateBaseModel
from django.contrib.auth import get_user_model
from .customers import Customers
from .sales_status import SalesStatus

User = get_user_model()

class PaymentMethodChoices(models.TextChoices):
    EFECTIVO = '1', _('Efectivo')
    TARJETA = '2', _('Tarjeta de Crédito')
    NEQUI = '3', _('Nequi')

class Sales(DateBaseModel):
    """
    Modelo para almacenar información sobre ventas realizadas.
    """
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, related_name="sales")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sales")
    payment_method = models.CharField(
        max_length=1,
        choices=PaymentMethodChoices.choices,
        default=PaymentMethodChoices.EFECTIVO
    )
    sale_status = models.ForeignKey(SalesStatus, on_delete=models.PROTECT)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created = models.DateTimeField(auto_now_add=True)  # Se establece al crear el objeto
    updated = models.DateTimeField(auto_now=True)       # Se actualiza al guardar el objeto

    def __str__(self):
        return f"Venta #{self.id} - Cliente: {self.customer.name} - Total: ${self.total}"

    class Meta(DateBaseModel.Meta):
        db_table = 'sales'
        managed = True
        verbose_name = 'sale'
        verbose_name_plural = 'sales'
