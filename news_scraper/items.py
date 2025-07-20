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
    pass

class ZoomitArticleItem(scrapy.Item):
    title = scrapy.Field()
    tags = scrapy.Field()
    published_at = scrapy.Field()
    cover_image = scrapy.Field()
    inline_images = scrapy.Field()
    content = scrapy.Field()
    source_url = scrapy.Field()
