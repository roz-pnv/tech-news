from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from core.models.base import TimestampedModel


class News(TimestampedModel):
    title = models.CharField(max_length=255)
    tags = models.ManyToManyField("Tag", related_name="news_items")
    slug = models.SlugField(unique=True, blank=True)
    body = models.TextField()
    summary = models.TextField(blank=True, null=True)
    source = models.CharField(max_length=255)
    published_at = models.DateTimeField()

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"
        ordering = ["-published_at"]
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["body"]),
        ]
        
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("news-detail", kwargs={"slug": self.slug})
        