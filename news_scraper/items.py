# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem

from news.models import News
from news.models import Tag
from news.models import NewsImage


class NewsScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class NewsItem(DjangoItem):
    django_model = News

class TagItem(DjangoItem):
    django_model = Tag

class TagItem(DjangoItem):
    django_model = NewsImage

