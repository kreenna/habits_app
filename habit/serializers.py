from rest_framework import serializers

from .models import Habit, Subscription


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ["id", "habit", "last_reminded"]
        read_only_fields = ["last_reminded"]
