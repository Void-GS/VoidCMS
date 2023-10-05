from voidcms.mdls.Client import Client
from rest_framework import serializers
from django.contrib.auth import authenticate


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = (
            "id",
            "email",
            "password",
            "phone",
            "name",
            "last_name",
            "address",
            "role",
        )
        extra_kwargs = {
            "password": {"write_only": True, "required": False},
            "name": {"required": False},
            "last_name": {"required": False},
            "address": {"required": False},
            "email": {"required": True},
            "phone": {"required": True},
        }

    def create(self, validated_data):
        is_first_user = not Client.objects.exists()

        if is_first_user:
            validated_data["role"] = "admin"
        
        user = Client.objects.create_user(
            username=validated_data["email"],
            email=validated_data["email"],
            password=validated_data["password"],
            phone=validated_data["phone"],
            name=validated_data.get("name", ""),
            last_name=validated_data.get("last_name", ""),
            address=validated_data.get("address", ""),
            role=validated_data.get("role", "user"),
        )
        return user


class EmailLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(label="Email")
    password = serializers.CharField(label="Password", style={"input_type": "password"})

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(username=email, password=password)

            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User account is disabled.")
            else:
                raise serializers.ValidationError(
                    "Unable to log in with provided credentials."
                )
        else:
            raise serializers.ValidationError("Must include 'email' and 'password'.")

        attrs["user"] = user
        return attrs
