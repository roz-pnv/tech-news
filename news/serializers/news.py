from rest_framework import serializers

from news.models import News


class NewsListSerializer(serializers.ModelSerializer):
    summary = serializers.ReadOnlyField()
    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name' 
    )

    class Meta:
        model = News
        fields = ['id', 'title', 'slug', 'summary', 'published_at', 'tags']
