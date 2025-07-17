from django.db import models
from django.urls import reverse

from core.models.base import TimestampedModel

class News(TimestampedModel):
    title = models.CharField(max_length=255)
    tags = models.ManyToManyField("Tag", related_name="news_items")
    slug = models.SlugField(unique=True, blank=True)
    body = models.TextField()
    source = models.CharField(max_length=255)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"
        ordering = ["-published_at"]
        indexes = [
            models.Index(fields=["title"]),
        ]
        
    def __str__(self):
        return self.title
    
    def __repr__(self):
        return f"<News id={self.pk} title='{self.title}'>"

    def get_absolute_url(self):
        return reverse("news-detail", kwargs={"slug": self.slug})
    
    @property
    def summary(self):
        return f"{self.title} - {self.body[:150]}..."
        