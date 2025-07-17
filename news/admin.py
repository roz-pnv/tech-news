from django.contrib import admin

from .models.news import News
from .models.news_image import NewsImage
from .models.tag import Tag

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'published_at']
    filter_horizontal = ['tags']
    
admin.site.register(NewsImage)
admin.site.register(Tag)
