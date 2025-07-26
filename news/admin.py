from django.contrib import admin

from .models.news import News
from .models.news_image import NewsImage
from .models.tag import Tag

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'published_at']
    filter_horizontal = ['tags']

@admin.register(NewsImage)
class NewsImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'news','is_main']
    
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

