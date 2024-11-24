from django.db import models
from django.utils.translation import gettext_lazy as _


class SalesReportTypeChoices(models.TextChoices):
    GENERAL = 'GENERAL', _('GENERAL')
    GATEGORY = 'GATEGORY', _('POR CATEGORIAS')
    PRODUCT = 'PRODUCT', _('POR PRODUCTOS')
    CUSTOMER = 'CUSTOMER', _('CLIENTE')