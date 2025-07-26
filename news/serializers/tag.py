from rest_framework import serializers

from news.models import Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
        
		
class TagCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
        extra_kwargs = {
            'name': {'required': True}
        }

    def create(self, validated_data):
        tag, created = Tag.objects.get_or_create(name=validated_data['name'])
        return tag


class TagUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Tag
        fields = ['id', 'name']
        