from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from news.models import News
from news.models import Tag
from news.models import NewsImage

class NewsListViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("news-list-explicit")

        self.tag_ai = Tag.objects.create(name="ai")
        self.tag_fashion = Tag.objects.create(name="fashion")

        self.news1 = News.objects.create(
            title="Published News",
            body="Visible content",
            source="BBC",
            slug="published-news",
            published_at=timezone.now()
        )
        self.news1.tags.add(self.tag_ai)

        self.news2 = News.objects.create(
            title="Fashion Week Highlights",
            body="Runway trends dominate.",
            source="Vogue",
            slug="fashion-week",
            published_at=timezone.now()
        )
        self.news2.tags.add(self.tag_fashion)

        self.news3 = News.objects.create(
            title="Future News",
            body="This will be visible tomorrow.",
            source="CNN",
            slug="future-news",
            published_at=timezone.now() + timezone.timedelta(days=1)
        )

    def test_list_view_returns_only_published_news(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [item["title"] for item in response.data["results"]]
        self.assertIn("Published News", titles)
        self.assertIn("Fashion Week Highlights", titles)
        self.assertNotIn("Future News", titles)

    def test_filter_by_tags(self):
        response = self.client.get(self.url, {"tags": "fashion"})
        titles = [item["title"] for item in response.data["results"]]
        self.assertIn("Fashion Week Highlights", titles)
        self.assertNotIn("Published News", titles)

    def test_filter_contains(self):
        response = self.client.get(self.url, {"contains": "Runway"})
        titles = [item["title"] for item in response.data["results"]]
        self.assertIn("Fashion Week Highlights", titles)
        self.assertNotIn("Published News", titles)

    def test_filter_not_contains(self):
        response = self.client.get(self.url, {"not_contains": "Visible"})
        titles = [item["title"] for item in response.data["results"]]
        self.assertIn("Fashion Week Highlights", titles)
        self.assertNotIn("Published News", titles)

    def test_combined_filters(self):
        response = self.client.get(self.url, {
            "tags": "ai",
            "contains": "Visible",
            "not_contains": "Runway"
        })
        titles = [item["title"] for item in response.data["results"]]
        self.assertEqual(titles, ["Published News"])


class NewsCreateViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = get_user_model().objects.create_user(username='tester', password='pass1234')
        self.client.force_authenticate(user=self.user)

        self.url = reverse("news-create")  

        self.tag_ai = Tag.objects.create(name="ai")
        self.image_data = {
            "image_url": "https://example.com/image.jpg",
            "alt_text": "sample image",
            "is_main": True,
            "position": 1
        }

        self.payload = {
            "title": "New AI Breakthrough",
            "body": "A new discovery in AI research...",
            "source": "TechCrunch",
            "published_at": str(timezone.now()),
            "tags": [self.tag_ai.id],
            "images": [self.image_data]
        }

    def test_create_news_with_image_and_tags(self):
        response = self.client.post(self.url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        news = News.objects.get(title="New AI Breakthrough")
        self.assertEqual(news.body, "A new discovery in AI research...")
        self.assertEqual(news.source, "TechCrunch")
        self.assertEqual(news.tags.count(), 1)

        self.assertEqual(news.images.count(), 1)
        image = news.images.first()
        self.assertEqual(image.image_url, "https://example.com/image.jpg")
        self.assertTrue(image.is_main)
