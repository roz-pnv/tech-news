from django.db import models

from core.models.base import TimestampedModel  

class NewsImage(TimestampedModel):
    news = models.ForeignKey("News", on_delete=models.CASCADE, related_name="images")
    image_file = models.ImageField(upload_to="news/images/", null=True, blank=True)
    image_url = models.URLField(max_length=1000, null=True, blank=True)
    alt_text = models.CharField(max_length=255, null=True, blank=True)
    is_main = models.BooleanField(default=False)
    position = models.PositiveIntegerField(
        null=True, 
        blank=True,
        help_text="Order of images for each news item",
    )

    class Meta:
        verbose_name = "News Image"
        verbose_name_plural = "News Images"
        ordering = ["news", "position", "-created_at"]
        unique_together = ("news", "position") 

    def __str__(self):
        return f"{self.alt_text or 'Image'} for {self.news.title}"

    def __repr__(self):
        return f"<NewsImage id={self.pk} news_id={self.news_id} is_main={self.is_main}>"

    def get_image(self):
        if self.image_file:
            return self.image_file.url
        return self.image_url
    
    def save(self, *args, **kwargs):
        if self.position is None:
            last = NewsImage.objects.filter(news=self.news).aggregate(models.Max("position"))["position__max"]
            self.position = (last or 0) + 1

        if self.is_main:
            NewsImage.objects.filter(news=self.news, is_main=True).exclude(pk=self.pk).update(is_main=False)

        if not NewsImage.objects.filter(news=self.news, is_main=True).exists():
            self.is_main = True

        super().save(*args, **kwargs)

