from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.reverse import reverse

from news.models import News
from news.models import NewsImage
from news.models import Tag
from news.serializers.news_image import NewsImageSerializer
from news.serializers.news_image import NewsImageCreateSerializer
from news.serializers.news_image import NewsImageUpdateSerializer
from news.serializers.tag import TagSerializer
from news.serializers.tag import TagCreateSerializer
from news.serializers.tag import TagUpdateSerializer


class NewsListSerializer(serializers.ModelSerializer):
    summary = serializers.SerializerMethodField()
    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )
    cover_image_url = serializers.SerializerMethodField()
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = ['id', 'title', 'detail_url', 'summary', 'published_at', 'tags', 'cover_image_url']

    @extend_schema_field(serializers.URLField(allow_null=True))
    def get_cover_image_url(self, obj):
        main_image = obj.images.filter(is_main=True).first()
        return main_image.get_image() if main_image else None

    @extend_schema_field(serializers.CharField())
    def get_summary(self, obj):
        return obj.summary
    
    @extend_schema_field(serializers.URLField())
    def get_detail_url(self, obj):
        request = self.context.get('request')
        return reverse('news-detail', kwargs={'slug': obj.slug}, request=request)


class NewsCreateSerializer(serializers.ModelSerializer):
    tags = TagCreateSerializer(many=True)
    images = NewsImageCreateSerializer(many=True, required=False)

    class Meta:
        model = News
        fields = ['title', 'body', 'source', 'published_at', 'tags', 'images']

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        tags_data = validated_data.pop('tags', [])

        news = News.objects.create(**validated_data)

        tag_instances = []
        for tag_data in tags_data:
            tag = TagCreateSerializer().create(tag_data)
            tag_instances.append(tag)
        news.tags.set(tag_instances)

        for image_data in images_data:
            NewsImage.objects.create(news=news, **image_data)

        return news
    


class NewsUpdateSerializer(serializers.ModelSerializer):
    tags = TagUpdateSerializer(many=True, required=False)
    images = NewsImageUpdateSerializer(many=True, required=False)

    class Meta:
        model = News
        fields = ['title', 'body', 'tags', 'images', 'published_at']

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', None)
        images_data = validated_data.pop('images', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if tags_data is not None:
            tag_instances = []
            for tag in tags_data:
                tag_id = tag.get('id')
                if tag_id:
                    obj = Tag.objects.filter(id=tag_id).first()
                    if obj:
                        obj.name = tag.get('name', obj.name)
                        obj.save()
                        tag_instances.append(obj)
                else:
                    obj, _ = Tag.objects.get_or_create(name=tag['name'])
                    tag_instances.append(obj)
            instance.tags.set(tag_instances)

        if images_data is not None:
            for img in images_data:
                img_id = img.pop('id', None) 
                if img_id:
                    NewsImage.objects.filter(id=img_id, news=instance).update(**img)
                else:
                    NewsImage.objects.create(news=instance, **img)

        return instance
    

class NewsDetailSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    images = NewsImageSerializer(many=True, read_only=True)

    class Meta:
        model = News
        fields = ['id', 'title', 'tags', 'body', 'images', 'published_at']
    