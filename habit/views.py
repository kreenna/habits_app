from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from habit.models import Habit
from habit.paginators import HabitsPagination
from habit.serializers import HabitSerializer
from users.permissions import IsModerator, IsOwner


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    pagination_class = HabitsPagination

    def get_queryset(self):
        user = self.request.user
        # если пользователь - модератор, видит все курсы
        if user.groups.filter(name="managers").exists():
            return Habit.objects.all().order_by("id")
        # если не модератор - видит только свои курсы (созданные самим пользователем)
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
