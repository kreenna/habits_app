from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from habit.models import Habit, Subscription
from habit.paginators import HabitsPagination
from habit.serializers import HabitSerializer, SubscriptionSerializer
from users.permissions import IsModerator, IsOwner


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    pagination_class = HabitsPagination

    def get_queryset(self):
        user = self.request.user
        # если пользователь - модератор, видит все привычки
        if user.groups.filter(name="managers").exists():
            return Habit.objects.all().order_by("id")
        # если не модератор - видит только свои привычки (созданные самим пользователем)
        return Habit.objects.filter(user=self.request.user).order_by("id")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action in ["list", "retrieve", "update", "partial_update"]:
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action in ["create"]:
            # запрещаем модераторам создавать
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action in ["destroy"]:
            self.permission_classes = [IsAuthenticated, IsOwner]
        else:
            self.permission_classes = [IsAuthenticated]

        return [permission() for permission in self.permission_classes]


class PublicHabitsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = HabitSerializer
    pagination_class = HabitsPagination

    def get_queryset(self):
        return Habit.objects.filter(is_public=True).order_by("id")


class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        return Subscription.objects.filter(subscriber=self.request.user).order_by("id")

    def create(self, request, *args, **kwargs):
        user = request.user
        habit_id = request.data.get("habit")
        habit_item = get_object_or_404(Habit, id=habit_id)

        Subscription.objects.create(subscriber=user, habit=habit_item)
        return Response({"message": "подписка добавлена"}, status=status.HTTP_201_CREATED)
