from django.db import models
from django.utils.translation import gettext_lazy as _


class SalesReportTypeChoices(models.TextChoices):
    GENERAL = 'GENERAL', _('GENERAL')
    GATEGORY = 'GATEGORY', _('POR CATEGORIAS')
    PRODUCT = 'PRODUCT', _('POR PRODUCTOS')
    CUSTOMER = 'CUSTOMER', _('POR CLIENTE')


class ReportResponseFormatChoices(models.TextChoices):
    JSON = 'JSON'
    EXCEL = 'EXCEL'


class PurchaseReportTypeChoices(models.TextChoices):
    GENERAL = 'GENERAL', _('GENERAL')
    GATEGORY = 'ARTICLE_TYPE', _('POR TIPO ARTICULO')
    PRODUCT = 'ARTICLE', _('POR ARTICULO')
    CUSTOMER = 'SUPPLIER', _('POR PROVEEDOR')