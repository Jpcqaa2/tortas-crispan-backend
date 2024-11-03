
# Django
from django.db import models

from apps.utils.models.base import DateBaseModel


class Articles(DateBaseModel):

    name = models.CharField(max_length=150)
    presentation = models.CharField(max_length=100, null=True, blank=True)
    reference = models.CharField(max_length=100, null=True, blank=True)
    is_disposible = models.BooleanField(default=False)
    article_type = models.ForeignKey('purchases.ArticleTypes', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta(DateBaseModel.Meta):
        db_table = 'articles'
        managed = True
        verbose_name = 'article'
        verbose_name_plural = 'articles'
