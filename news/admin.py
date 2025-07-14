from django.contrib import admin

from .models.news import News
from .models.news_image import NewsImage
from .models.tag import Tag

admin.site.register(News)
admin.site.register(NewsImage)
admin.site.register(Tag)
