
from django.db import models

# Utils
from apps.utils.models.base import DateBaseModel


class SalesDetails(DateBaseModel):
    """
    Modelo para almacenar los detalles de una venta específica,
    incluyendo productos, cantidad y precio.
    """
    sale = models.ForeignKey('sales.Sales', on_delete=models.CASCADE)
    product = models.ForeignKey('sales.Products', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    unit_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"Detalle Venta #{self.sale.id} - Producto: {self.product.name} - Cantidad: {self.quantity}"

    class Meta(DateBaseModel.Meta):
        db_table = 'sales_details'
        managed = True
        verbose_name = 'sale detail'
        verbose_name_plural = 'sales details'
