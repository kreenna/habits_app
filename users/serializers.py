from rest_framework import serializers

from .models import CustomUser
from habit.serializers import HabitSerializer


class UserSerializer(serializers.ModelSerializer):
    habits = HabitSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ["id", "email", "phone_number", "avatar", "country", "habits"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data["email"],
            phone_number=validated_data.get("phone_number", ""),
            country=validated_data.get("country", ""),
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
