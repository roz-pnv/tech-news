from rest_framework import serializers

from news.models import NewsImage

class NewsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsImage
        fields = ['image_file', 'image_url', 'alt_text', 'is_main', 'position']
        extra_kwargs = {
            'image_file': {'required': False, 'allow_null': True},
            'image_url': {'required': False, 'allow_null': True},
            'alt_text': {'required': False, 'allow_blank': True},
            'is_main': {'required': False},
            'position': {'required': False}
        }

    def validate(self, attrs):
        if attrs.get('image_file') or attrs.get('image_url'):
            return attrs
        raise serializers.ValidationError("Either image_file or image_url must be provided.")
