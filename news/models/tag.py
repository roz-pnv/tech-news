from django.db import models
from django.utils.text import slugify
from django.urls import reverse

from core.models.base import TimestampedModel  

class Tag(TimestampedModel):
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="The name of the tag (must be unique)"
    )
    slug = models.SlugField(
        max_length=120,
        unique=True,
        blank=True,
        help_text="URL-friendly version of the tag name (auto-generated if left blank)"
    )

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Tag id={self.pk} name='{self.name}'>"
    
    def get_absolute_url(self):
    	return reverse("tag-news-list", kwargs={"slug": self.slug})
