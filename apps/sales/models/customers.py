# apps/sales/models/customers.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.utils.models.base import DateBaseModel

class IdentificationTypeChoices(models.TextChoices):
    CC = 'CC', _('Cédula de Ciudadanía')
    CE = 'CE', _('Cédula de Extranjería')

class Customers(DateBaseModel):
    """
    Modelo para almacenar información de clientes.
    """
    name = models.CharField(max_length=150)
    identification_type = models.CharField(
        max_length=2,
        choices=IdentificationTypeChoices.choices
    )
    identification_number = models.CharField(max_length=20)
    cell_phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=100, null=True)
    birth_date = models.DateField(null=True, blank=True)
    residential_address = models.CharField(max_length=100, null=True)
    city = models.ForeignKey('utils.City', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta(DateBaseModel.Meta):
        db_table = 'customers'
        managed = True
        verbose_name = 'customer'
        verbose_name_plural = 'customers'
