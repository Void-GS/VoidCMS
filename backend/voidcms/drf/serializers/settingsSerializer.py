from rest_framework import serializers
from voidcms.models import Settings
from voidcms.models import Image

from voidcms.drf.serializers.imageSerializer import ImageSerializer


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = '__all__'

    app_logo_upload = serializers.FileField(
        max_length=100000, allow_empty_file=False, required=False, write_only=True)
    app_favicon_upload = serializers.FileField(
        max_length=100000, allow_empty_file=False, required=False, write_only=True)
    app_background_upload = serializers.FileField(
        max_length=100000, allow_empty_file=False, required=False, write_only=True)

    def create(self, validated_data):
        backgorund_data = validated_data.pop('app_background_upload', None)
        logo_data = validated_data.pop('app_logo_upload', None)
        favicon_data = validated_data.pop('app_favicon_upload', None)

        settings = Settings.objects.create(**validated_data)

        if backgorund_data:
            settings.app_background = Image.objects.create(
                name=backgorund_data.name, url=backgorund_data)

        if logo_data:
            settings.app_logo = Image.objects.create(
                name=logo_data.name, url=logo_data)

        if favicon_data:
            settings.app_favicon = Image.objects.create(
                name=favicon_data.name, url=favicon_data)

        settings.save()
        return settings

    def update(self, instance, validated_data):
        background_data = validated_data.pop('app_background_upload', None)
        logo_data = validated_data.pop('app_logo_upload', None)
        favicon_data = validated_data.pop('app_favicon_upload', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if background_data is not None:
            if instance.app_background:
                instance.app_background.delete()
            instance.app_background = Image.objects.create(
                name=background_data.name, url=background_data)

        if logo_data is not None:
            if instance.app_logo:
                instance.app_logo.delete()
            instance.app_logo = Image.objects.create(
                name=logo_data.name, url=logo_data)

        if favicon_data is not None:
            if instance.app_favicon:
                instance.app_favicon.delete()
            instance.app_favicon = Image.objects.create(
                name=favicon_data.name, url=favicon_data)

        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.app_logo is not None:
            representation['app_logo'] = ImageSerializer(
                instance.app_logo).data
        if instance.app_favicon is not None:
            representation['app_favicon'] = ImageSerializer(
                instance.app_favicon).data
        if instance.app_background is not None:
            representation['app_background'] = ImageSerializer(
                instance.app_background).data
        return representation
