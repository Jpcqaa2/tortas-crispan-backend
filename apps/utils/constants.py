from django.db import models
from django.utils.translation import gettext_lazy as _


class PaymentMethodChoices(models.TextChoices):
    EFECTIVO = '1',_('EFECTIVO')
    NEQUI = '2',_('NEQUI')
    BANCOLOMBIA = '3',_('BANCOLOMBIA')


class MeasurementUnitChoices(models.TextChoices):
    GRAMO = '1',_('Gramos')
    KILO_GRAMO = '2',_('Kilo Gramo')
    LIBRA = '3',_('Libra')
    LITRO = '4',_('Litro')
    UNIDAD = '5',_('Unidad')