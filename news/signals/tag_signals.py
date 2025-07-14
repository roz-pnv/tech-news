from django.db.models.signals import pre_save
from django.dispatch import receiver

from news.models import Tag
from utils.slug import generate_unique_slug

@receiver(pre_save, sender=Tag)
def auto_generate_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = generate_unique_slug(instance, source_field='name')
