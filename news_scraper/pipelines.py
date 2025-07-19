# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from django.utils import timezone
from asgiref.sync import sync_to_async

from news.models import News
from news.models import Tag
from news.models import NewsImage


class NewsCreationPipeline:
    async def process_item(self, item, spider):
        await sync_to_async(self.save_item, thread_sensitive=True)(item)
        return item

    def save_item(self, item):
        news = News.objects.create(
            title=item.get("title"),
            body=item.get("content", "None"),
            source=item.get("source_url"),
            published_at = timezone.make_aware(item.get("published_at")),
        )

        for tag_name in item.get("tags", []):
            tag_obj, _ = Tag.objects.get_or_create(name=tag_name.strip())
            news.tags.add(tag_obj)

        cover = item.get("cover_image")
        if cover and cover.get("url"):
            NewsImage.objects.create(
                news=news,
                image_url=cover["url"],
                alt_text=cover.get("caption", "None"),
                is_main=True,
            )

        for idx, image in enumerate(item.get("inline_images", [])):
            NewsImage.objects.create(
                news=news,
                image_url=image.get("url"),
                alt_text=image.get("caption", "None"),
                is_main=False,
                position=idx+2,
            )

