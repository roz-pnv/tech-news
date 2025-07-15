from django.test import TestCase
from django.utils import timezone

from news.models import News
from news.models import NewsImage
from news.models import Tag

class NewsModelTest(TestCase):
    def setUp(self):
        self.news = News.objects.create(
            title="AI Revolution",
            body="Artificial intelligence is transforming industries.",
            source="TechCrunch",
            published_at=timezone.now()
        )

    def test_str_returns_title(self):
        self.assertEqual(str(self.news), "AI Revolution")

    def test_repr_contains_id_and_title(self):
        representation = repr(self.news)
        self.assertTrue(representation.startswith("<News id="))
        self.assertIn("title='AI Revolution'", representation)

    # def test_get_absolute_url_contains_slug(self):
    #     url = self.news.get_absolute_url()
    #     self.assertIn("ai-revolution", url)

    def test_summary_truncates_body(self):
        summary = self.news.summary
        self.assertTrue(summary.startswith("AI Revolution -"))
        self.assertTrue(summary.endswith("..."))
        self.assertLessEqual(len(summary), 180)


class NewsImageModelTest(TestCase):
    def setUp(self):
        self.news = News.objects.create(
            title="Test News",
            body="Some content",
            source="Source",
            published_at=timezone.now()
        )

    def test_str_returns_alt_text_or_default(self):
        img = NewsImage.objects.create(news=self.news, alt_text="Header Image")
        self.assertEqual(str(img), "Header Image for Test News")

        img2 = NewsImage.objects.create(news=self.news, alt_text="")
        self.assertEqual(str(img2), "Image for Test News")

    def test_repr_format(self):
        img = NewsImage.objects.create(news=self.news, alt_text="Thumb", is_main=True)
        representation = repr(img)
        self.assertIn("id=", representation)
        self.assertIn("news_id=", representation)
        self.assertIn("is_main=True", representation)

    def test_get_image_returns_image_url_when_file_not_set(self):
        img = NewsImage.objects.create(news=self.news, image_url="http://example.com/image.jpg", alt_text="Image")
        self.assertEqual(img.get_image(), "http://example.com/image.jpg")

    def test_save_sets_position_and_main_flag(self):
        img1 = NewsImage.objects.create(news=self.news, alt_text="First", is_main=True)
        img2 = NewsImage.objects.create(news=self.news, alt_text="Second", is_main=True)

        img1.refresh_from_db()
        img2.refresh_from_db()

        self.assertEqual(img1.is_main, False)
        self.assertEqual(img2.is_main, True)
        self.assertEqual(img1.position, 1)
        self.assertEqual(img2.position, 2)

    def test_save_sets_default_main_if_none_exists(self):
        img = NewsImage.objects.create(news=self.news, alt_text="Solo Image")
        self.assertTrue(img.is_main)


class TagModelTest(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name="Science")

    def test_str_returns_name(self):
        self.assertEqual(str(self.tag), "Science")

    def test_repr_contains_id_and_name(self):
        representation = repr(self.tag)
        self.assertIn(f"id={self.tag.pk}", representation)
        self.assertIn("name='Science'", representation)

    # def test_get_absolute_url_contains_slug(self):
    #     url = self.tag.get_absolute_url()
    #     self.assertIn("science", url)
