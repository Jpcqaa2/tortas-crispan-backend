
# Django
from django.db import models

from apps.utils.models.base import DateBaseModel


class ArticleTypes(DateBaseModel):

    name = models.CharField(max_length=150)
    description = models.CharField(max_length=250, null=False)

    def __str__(self):
        return self.name

    class Meta(DateBaseModel.Meta):
        db_table = 'article_types'
        managed = True
        verbose_name = 'article types'
        verbose_name_plural = 'article types'
