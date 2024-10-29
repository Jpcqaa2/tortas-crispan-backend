# apps/sales/models/sales_details.py
from django.db import models
from apps.utils.models.base import DateBaseModel
from .sales import Sales
from .products import Products

class SalesDetails(DateBaseModel):
    """
    Modelo para almacenar los detalles de una venta específica,
    incluyendo productos, cantidad y precio.
    """
    sale = models.ForeignKey(Sales, on_delete=models.CASCADE, related_name="sales_details")
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="sales_details")
    quantity = models.IntegerField(default=1)
    unit_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created = models.DateTimeField(auto_now_add=True)  # Se establece al crear el objeto
    updated = models.DateTimeField(auto_now=True)       # Se actualiza al guardar el objeto

    def __str__(self):
        return f"Detalle Venta #{self.sale.id} - Producto: {self.product.name} - Cantidad: {self.quantity}"

    class Meta(DateBaseModel.Meta):
        db_table = 'sales_details'
        managed = True
        verbose_name = 'sale detail'
        verbose_name_plural = 'sales details'
