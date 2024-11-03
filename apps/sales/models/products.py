
# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Utils
from apps.utils.constants import MeasurementUnitChoices
from apps.utils.models.base import DateBaseModel


class Products(DateBaseModel):
    """
    Modelo para almacenar información de productos.
    """
    name = models.CharField(max_length=150)
    quantity = models.IntegerField(default=0)
    measurement_unit = models.CharField(
        max_length=4,
        choices=MeasurementUnitChoices.choices,
        default=MeasurementUnitChoices.UNIDAD
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, null=True, blank=True)
    category = models.ForeignKey('sales.Categories', on_delete=models.CASCADE)
    photo = models.ImageField(
        null=True,
        upload_to='files/products/pictures/'
    )
    featured_product = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta(DateBaseModel.Meta):
        db_table = 'products'
        managed = True
        verbose_name = 'product'
        verbose_name_plural = 'products'
