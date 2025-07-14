from django.db.models.signals import pre_save
from django.dispatch import receiver

from news.models.news import News
from utils.slug import generate_unique_slug 

@receiver(pre_save, sender=News)
def auto_generate_slug(sender, instance, **kwargs):
    if not instance.slug and instance.title:
        instance.slug = generate_unique_slug(instance, instance.title)
