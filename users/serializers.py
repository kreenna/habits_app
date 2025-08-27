from rest_framework import serializers

from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "phone_number", "avatar", "country"]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data["email"],
            phone_number=validated_data.get("phone_number", ""),
            country=validated_data.get("country", ""),
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
