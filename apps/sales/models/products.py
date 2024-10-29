# apps/sales/models/products.py

# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Utils
from apps.utils.models.base import DateBaseModel

# Importación del modelo Categories
from apps.sales.models.categories import Categories



class MeasurementUnitChoices(models.TextChoices):
    GRAMO = 'g', _('Gramo')
    KILOGRAMO = 'kg', _('Kilogramo')
    LITRO = 'l', _('Litro')
    UNIDAD = 'unit', _('Unidad')

class Products(DateBaseModel):
    """
    Modelo para almacenar información de productos.
    """
    name = models.CharField(max_length=150)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    measurement_unit = models.CharField(
        max_length=4,
        choices=MeasurementUnitChoices.choices,
        default=MeasurementUnitChoices.UNIDAD
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, null=True, blank=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    photo = models.URLField(max_length=255, null=True, blank=True)
    featured_product = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta(DateBaseModel.Meta):
        db_table = 'products'
        managed = True
        verbose_name = 'product'
        verbose_name_plural = 'products'
