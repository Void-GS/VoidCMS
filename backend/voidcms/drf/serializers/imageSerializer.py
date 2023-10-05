
from rest_framework import serializers
from voidcms.models import Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'url', 'name']

class ImageUploadSerializer(serializers.Serializer):
    images = serializers.ListField(child=serializers.FileField(max_length=100000, allow_empty_file=False))
