from django.test import TestCase
from django.utils import timezone

from news.models import News
from scraper_control.models import ScrapedArticle  

class ScrapedArticleModelTest(TestCase):
    def setUp(self):
        self.news = News.objects.create(
            title="Test News",
            body="Some body",
            source="TestSource",
            published_at=timezone.now()
        )

    def test_create_scraped_article_with_valid_url(self):
        article = ScrapedArticle.objects.create(
            url="https://example.com/article1",
            mapped_to=self.news
        )
        self.assertEqual(str(article), "https://example.com/article1")
        self.assertEqual(article.mapped_to, self.news)

    def test_scraped_article_url_uniqueness(self):
        ScrapedArticle.objects.create(url="https://example.com/article2")
        with self.assertRaises(Exception):
            ScrapedArticle.objects.create(url="https://example.com/article2")  # duplicated URL

    def test_scraped_article_can_be_unmapped(self):
        article = ScrapedArticle.objects.create(url="https://example.com/unmapped")
        self.assertIsNone(article.mapped_to)
