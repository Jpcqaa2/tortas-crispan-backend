# apps/sales/models/sales_status.py
from django.db import models
from apps.utils.models.base import DateBaseModel

class SalesStatus(DateBaseModel):
    """
    Modelo para representar el estado de una venta.
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta(DateBaseModel.Meta):
        db_table = 'sales_status'
        managed = True
        verbose_name = 'sales status'
        verbose_name_plural = 'sales statuses'
