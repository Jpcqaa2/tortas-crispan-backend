
# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.utils.models.base import DateBaseModel


class Suppliers(DateBaseModel):

    name = models.CharField(max_length=150)
    cell_phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=100, null=True)
    establishment_address = models.CharField(max_length=100, null=True)
    city = models.ForeignKey('utils.City', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta(DateBaseModel.Meta):
        db_table = 'suppliers'
        managed = True
        verbose_name = 'supplier'
        verbose_name_plural = 'suppliers'
