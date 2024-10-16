from django.contrib import admin

from apps.purchases.models.article_types import ArticleTypes
from apps.purchases.models.articles import Articles
from apps.purchases.models.purchases import Purchases
from apps.purchases.models.purchases_details import PurchasesDetails
from apps.purchases.models.suppliers import Suppliers

# Register your models here.

admin.site.register(Suppliers)
admin.site.register(Articles)
admin.site.register(ArticleTypes)
admin.site.register(Purchases)
admin.site.register(PurchasesDetails)