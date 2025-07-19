from django.db import models

from core.models.base import TimestampedModel
from news.models import News


class ScrapedArticle(TimestampedModel):
    url = models.URLField(unique=True)
    mapped_to = models.ForeignKey(News, null=True, blank=True, on_delete=models.SET_NULL)
        
    def __str__(self):
        return self.url
