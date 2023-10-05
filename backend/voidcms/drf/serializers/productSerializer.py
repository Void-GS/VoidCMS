from voidcms.models import Product,Image, Complectation, Category
from rest_framework import serializers
from voidcms.drf.serializers.imageSerializer import ImageSerializer
import json

class ComplectationField(serializers.Field):
    def to_internal_value(self, data):
        try:
            complectations = json.loads(data)
            if isinstance(complectations, list):
                return complectations
        except json.JSONDecodeError:
            pass
        raise serializers.ValidationError("Invalid complectations format")

class ComplectationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complectation
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    images_upload = serializers.ListField(
        child=serializers.FileField(max_length=100000, allow_empty_file=False),
        write_only=True,
        required=False
    )

    category = serializers.CharField(required=False, allow_null=True)

    complectations = ComplectationField(write_only=True, required=False)


    def create(self, validated_data):
        del validated_data['images']
        images_data = validated_data.pop('images_upload', [])
        complectations_data = validated_data.pop('complectations', [])

        if 'category' in validated_data and validated_data['category'] == "undefined":
            del validated_data['category']
        else:
            category_value = validated_data.get('category')
            if category_value is not None:
                try:
                    category = Category.objects.get(pk=category_value)
                    validated_data['category'] = category
                except Category.DoesNotExist:
                    category = None
                    del validated_data['category']

        product = Product.objects.create(**validated_data)

    
        if images_data:
            for image_data in images_data:
                product.images.add(Image.objects.create(name=image_data.name, url=image_data))

        if complectations_data:
            for complectation in complectations_data:
                product.complectations.add(Complectation.objects.create(type=complectation['type'], value=complectation['value'], price_change=complectation['price_change']))
        
        return product
    
    def update(self, instance, validated_data):
        images_data = validated_data.pop('images_upload', [])
        del validated_data['images']

        if 'category' in validated_data and validated_data['category'] == "undefined":
            instance.category = None 
            del validated_data['category']
        else:
            category_value = validated_data.get('category')
            if category_value is not None:
                try:
                    instance.category = Category.objects.get(pk=category_value)
                except Category.DoesNotExist:
                    instance.category = None
                else:
                    del validated_data['category']

        complectations_data = validated_data.pop('complectations', [])
        instance.complectations.all().delete()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if images_data:
            for image_data in images_data:
                instance.images.add(Image.objects.create(name=image_data.name, url=image_data))
        
        if complectations_data:
            for complectation in complectations_data:
                instance.complectations.add(Complectation.objects.create(type=complectation['type'], value=complectation['value'], price_change=complectation['price_change']))

        instance.save()
        return instance
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = instance.category.pk if instance.category else None
        representation['images'] = ImageSerializer(instance.images.all(), many=True).data
        representation['complectations'] = ComplectationSerializer(instance.complectations.all(), many=True).data
        return representation