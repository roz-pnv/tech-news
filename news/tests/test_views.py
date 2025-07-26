from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from news.models import News
from news.models import Tag
from news.models import NewsImage
from news.serializers.news import NewsListSerializer

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
            published_at=timezone.now()
        )
        self.news1.tags.add(self.tag_ai)

        self.news2 = News.objects.create(
            title="Fashion Week Highlights",
            body="Runway trends dominate.",
            source="Vogue",
            published_at=None
        )
        self.news2.tags.add(self.tag_fashion)

        self.news3 = News.objects.create(
            title="Future News",
            body="This will be visible tomorrow.",
            source="CNN",
            published_at=timezone.now() + timezone.timedelta(days=1)
        )

    def test_list_view_returns_only_news_with_non_null_published_at(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        titles = [item["title"] for item in response.data["results"]]

        self.assertIn("Published News", titles)
        self.assertIn("Future News", titles)
        self.assertNotIn("Fashion Week Highlights", titles) 

    def test_filter_by_tags_excludes_unpublished(self):
        response = self.client.get(self.url, {"tags": "fashion"})
        titles = [item["title"] for item in response.data["results"]]

        self.assertNotIn("Fashion Week Highlights", titles)
        self.assertNotIn("Published News", titles)

    def test_filter_contains_excludes_unpublished(self):
        response = self.client.get(self.url, {"contains": "Runway"})
        titles = [item["title"] for item in response.data["results"]]

        self.assertNotIn("Fashion Week Highlights", titles)
        self.assertNotIn("Published News", titles)

    def test_filter_not_contains_excludes_unpublished(self):
        response = self.client.get(self.url, {"not_contains": "Visible"})
        titles = [item["title"] for item in response.data["results"]]

        self.assertEqual(titles, []) 

    def test_combined_filters_respects_published_date(self):
        response = self.client.get(self.url, {
            "tags": "ai",
            "contains": "Visible",
            "not_contains": "Runway"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        titles = [item["title"] for item in response.data["results"]]

        self.assertEqual(titles, ["Published News"])


class NewsMutationViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username="rozhin", password="testpass123")
        self.client.force_authenticate(user=self.user)
        self.url = reverse("news-create")

    def test_create_news_with_tags_and_images(self):
        payload = {
            "title": "AI Revolution Begins",
            "body": "The rise of intelligent systems...",
            "source": "TechRadar",
            "published_at": timezone.now().isoformat(),
            "tags": [{"name": "AI"}, {"name": "Innovation"}],
            "images": [{
                "image_url": "https://example.com/img.jpg",
                "alt_text": "A futuristic image",
                "is_main": True
            }]
        }

        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "AI Revolution Begins")

    def test_update_news_title_and_tags(self):
        create_payload = {
            "title": "Initial Title",
            "body": "Some initial content",
            "source": "Wired",
            "published_at": timezone.now().isoformat(),
            "tags": [{"name": "Tech"}],
            "images": []
        }

        create_resp = self.client.post(self.url, create_payload, format="json")
        self.assertEqual(create_resp.status_code, status.HTTP_201_CREATED)
        slug = create_resp.data["title"].lower().replace(" ", "-")

        update_url = reverse("news-update", kwargs={"slug": slug})
        update_payload = {
            "title": "Updated Title",
            "body": "Updated content",
            "tags": [{"name": "UpdatedTech"}],
            "images": []
        }

        update_resp = self.client.put(update_url, update_payload, format="json")
        self.assertEqual(update_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(update_resp.data["title"], "Updated Title")

    def test_partial_update_news_title(self):
        create_payload = {
            "title": "Patch Target",
            "body": "Patchable content",
            "source": "TestSource",
            "published_at": timezone.now().isoformat(),
            "tags": [{"name": "Patch"}],
            "images": []
        }

        create_resp = self.client.post(self.url, create_payload, format="json")
        self.assertEqual(create_resp.status_code, status.HTTP_201_CREATED)
        slug = create_resp.data["title"].lower().replace(" ", "-")

        partial_url = reverse("news-partial-update", kwargs={"slug": slug})
        patch_payload = {
            "title": "Partially Updated Title"
        }

        patch_resp = self.client.patch(partial_url, patch_payload, format="json")
        self.assertEqual(patch_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_resp.data["title"], "Partially Updated Title")
        self.assertEqual(patch_resp.data["body"], "Patchable content")  

    def test_delete_news_removes_images(self):
        create_payload = {
            "title": "Delete Me",
            "body": "Content to be deleted",
            "source": "TestSource",
            "published_at": timezone.now().isoformat(),
            "tags": [{"name": "Delete"}],
            "images": [{
                "image_url": "https://example.com/delete.jpg",
                "alt_text": "to be removed",
                "is_main": True
            }]
        }

        create_resp = self.client.post(self.url, create_payload, format="json")
        self.assertEqual(create_resp.status_code, status.HTTP_201_CREATED)
        slug = create_resp.data["title"].lower().replace(" ", "-")

        delete_url = reverse("news-delete", kwargs={"slug": slug})
        delete_resp = self.client.delete(delete_url)
        self.assertEqual(delete_resp.status_code, status.HTTP_204_NO_CONTENT)


class NewsDetailViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username="rozhin", password="testpass123")
        self.client.force_authenticate(user=self.user)

        self.news = News.objects.create(
            title="Published News",
            body="Details of the news",
            source="BBC",
            published_at=timezone.now()
        )

        self.tag1 = Tag.objects.create(name="Tech")
        self.tag2 = Tag.objects.create(name="Innovation")
        self.news.tags.set([self.tag1, self.tag2])

        self.image = NewsImage.objects.create(
            news=self.news,
            image_url="https://example.com/pic.jpg",
            alt_text="published image",
            is_main=True,
            position=1
        )

    def test_retrieve_published_news_detail(self):
        slug = self.news.title.lower().replace(" ", "-")
        url = reverse("news-detail", kwargs={"slug": slug})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["title"], "Published News")
        self.assertEqual(len(response.data["tags"]), 2)
        self.assertEqual(response.data["images"][0]["alt_text"], "published image")
        self.assertEqual(response.data["images"][0]["is_main"], True)
        self.assertIn("published_at", response.data)