from django.utils.text import slugify

def generate_unique_slug(instance):
    model = instance.__class__
    base_slug = slugify(instance.title)
    slug = base_slug
    i = 1
    
    while model.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{i}"
        i += 1
        
    return slug
