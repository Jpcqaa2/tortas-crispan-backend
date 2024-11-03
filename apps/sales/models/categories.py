# Django
from django.db import models

# Utils
from apps.utils.models.base import DateBaseModel

class Categories(DateBaseModel):
    """
    Modelo para representar las categorías de productos.
    Hereda de DateBaseModel para contar con los campos 
    'id', 'created_at' y 'updated_at'.
    """
    name = models.CharField(max_length=150, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta(DateBaseModel.Meta):
        db_table = 'categories'
        managed = True
        verbose_name = 'category'
        verbose_name_plural = 'categories'
