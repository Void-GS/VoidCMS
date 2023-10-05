from rest_framework import serializers
from mptt.models import MPTTModel

from voidcms.models import Category
from voidcms.models import Image

from voidcms.drf.serializers.imageSerializer import ImageSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        extra_kwargs = {
            "parent": {"required": False},
        }

    image_upload = serializers.FileField(max_length=100000, allow_empty_file=False, required=False, write_only=True)

    def create(self, validated_data):
        image_data = validated_data.pop('image_upload', [])
        category = Category.objects.create(**validated_data)
        if image_data:
            category.image = Image.objects.create(name=image_data.name, url=image_data)
            category.save()
        return category

    def update(self, instance, validated_data):
        image_data = validated_data.pop('image_upload', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if image_data is not None:
            if instance.image:
                instance.image.delete()
            instance.image = Image.objects.create(name=image_data.name, url=image_data)
        instance.save()
        return instance


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.image is not None:
            representation['image'] = ImageSerializer(instance.image).data
        return representation
    

class CategoryTreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['children'] = CategoryTreeSerializer(instance.get_children(), many=True).data
        if instance.image is not None:
            representation['image'] = ImageSerializer(instance.image).data
        return representation