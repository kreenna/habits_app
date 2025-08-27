from django.core.exceptions import ValidationError
from django.db import models

from users.models import CustomUser


class Habit(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="habits", verbose_name="Пользователь")
    place = models.CharField(max_length=200, verbose_name="Место")
    time = models.DateTimeField(verbose_name="Время")
    action = models.TextField(verbose_name="Действие")
    related_habit = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)
    frequency_days = models.PositiveSmallIntegerField(default=1, verbose_name="Периодичность")
    reward = models.CharField(max_length=200, verbose_name="Награда")
    duration_seconds = models.PositiveSmallIntegerField(verbose_name="Продолжительность")
    is_pleasant = models.BooleanField(default=False, verbose_name="Приятность")
    is_public = models.BooleanField(default=False, verbose_name="Публичность")

    def __str__(self):
        return f"Я буду {self.action} в {self.time} в {self.place}"

    def clean(self):
        # исключить одновременное указание reward и related_habit
        if self.reward and self.related_habit:
            raise ValidationError("Не можете одновременно указать вознаграждение и связанную привычку.")
        # у приятной привычки не может быть reward или related_habit
        if self.is_pleasant and (self.reward or self.related_habit):
            raise ValidationError("У приятной привычки не должно быть вознаграждения или связанной привычки.")
        # ограничение времени выполнения
        if self.duration_seconds > 120:
            raise ValidationError("Время на выполнение не должно превышать 120 секунд.")
        # frequency_days от 1 до 7
        if not (1 <= self.frequency_days <= 7):
            raise ValidationError("Периодичность должна быть от 1 до 7 дней.")

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
