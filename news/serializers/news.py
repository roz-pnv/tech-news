from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from news.models import News
from news.models import NewsImage
from news.models import Tag
from news.serializers.news_image import NewsImageSerializer


class NewsListSerializer(serializers.ModelSerializer):
    summary = serializers.SerializerMethodField()
    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )
    cover_image_url = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = ['id', 'title', 'slug', 'summary', 'published_at', 'tags', 'cover_image_url']

    @extend_schema_field(serializers.URLField(allow_null=True))
    def get_cover_image_url(self, obj):
        main_image = obj.images.filter(is_main=True).first()
        return main_image.image_url if main_image else None

    @extend_schema_field(serializers.CharField())
    def get_summary(self, obj):
        return obj.summary


class NewsCreateSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    images = NewsImageSerializer(many=True, required=False)

    class Meta:
        model = News
        fields = ['title', 'body', 'source', 'published_at', 'tags', 'images']

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        tags_data = validated_data.pop('tags', [])
        news = News.objects.create(**validated_data)
        news.tags.set(tags_data)

        for image_data in images_data:
            NewsImage.objects.create(news=news, **image_data)

        return news
    