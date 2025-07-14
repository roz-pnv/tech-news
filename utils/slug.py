from django.utils.text import slugify

def generate_unique_slug(instance, source_field='title', slug_field='slug'):
    model = instance.__class__
    value = getattr(instance, source_field)
    base_slug = slugify(value)
    slug = base_slug
    i = 1

    while model.objects.filter(**{slug_field: slug}).exists():
        slug = f"{base_slug}-{i}"
        i += 1

    return slug
