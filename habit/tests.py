from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from habit.models import Habit, Subscription
from users.models import CustomUser


class HabitViewSetTests(APITestCase):

    def setUp(self):
        # создаем группы
        self.managers_group, _ = Group.objects.get_or_create(name="managers")

        # создаем пользователей
        self.manager = CustomUser.objects.create(email="manager@example.com", password="managerpass")
        self.manager.groups.add(self.managers_group)
        self.mod_habit = Habit.objects.create(
            user=self.manager, action="Mod action", time="11:00", place="Office", is_public=True
        )
        self.other_user = CustomUser.objects.create(email="non_owner@example.com", password="userpass")

        self.regular_user = CustomUser.objects.create(email="user@example.com", password="userpass")
        self.user_habit = Habit.objects.create(user=self.regular_user, action="User action", time="10:00",
                                               place="Home")

        # аутентификация клиентов
        self.client_mod = APIClient()
        self.client_mod.force_authenticate(user=self.manager)

        self.other_user_client = APIClient()
        self.other_user_client.force_authenticate(user=self.other_user)

        self.client_user = APIClient()
        self.client_user.force_authenticate(user=self.regular_user)

        self.list_url = "/habits/habits/"

    def test_list_habits_user_sees_own(self):
        response = self.client_user.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all(h["id"] == self.user_habit.id for h in response.data["results"]))

    def test_list_habits_moderator_sees_all(self):
        response = self.client_mod.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data["results"]), 2)

    def test_retrieve_habit_user_owner(self):
        url = f"/habits/habits/{self.user_habit.id}/"
        response = self.client_user.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.user_habit.id)

    def test_retrieve_habit_user_not_owner_forbidden(self):
        url = f"/habits/habits/{self.user_habit.id}/"
        response = self.other_user_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_habit_moderator_forbidden(self):
        data = {"user": self.manager, "action": "Forbidden action", "time": "13:00", "place": "Office"}
        response = self.client_mod.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_habit_owner_allowed(self):
        url = f"/habits/habits/{self.user_habit.id}/"
        data = {"action": "Updated action"}
        response = self.client_user.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["action"], data["action"])

    def test_update_habit_not_owner_forbidden(self):
        url = f"/habits/habits/{self.user_habit.id}/"
        data = {"action": "Try update"}
        response = self.other_user_client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_habit_owner_allowed(self):
        url = f"/habits/habits/{self.user_habit.id}/"
        response = self.client_user.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_habit_not_owner_forbidden(self):
        url = f"/habits/habits/{self.user_habit.id}/"
        response = self.other_user_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PublicHabitsViewSetTests(APITestCase):
    def setUp(self):
        self.regular_user = CustomUser.objects.create(email="user@example.com", password="userpass")

        # аутентификация клиентов
        self.client_user = APIClient()
        self.client_user.force_authenticate(user=self.regular_user)

        self.public_habit = Habit.objects.create(
            user=self.regular_user, action="Public action", time="10:00", place="Park", is_public=True
        )
        self.private_habit = Habit.objects.create(
            user=self.regular_user, action="Private action", time="11:00", place="Home", is_public=False
        )
        self.list_url = "/habits/public_habits/"

    def test_list_public_habits(self):
        response = self.client_user.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["id"], self.public_habit.id)

    def test_cannot_modify_public_habits(self):
        response = self.client_user.post(self.list_url, {"action": "New"})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class SubscriptionViewSetTests(APITestCase):
    def setUp(self):
        self.regular_user = CustomUser.objects.create(email="user@example.com", password="userpass")
        self.other_user = CustomUser.objects.create(email="non_owner@example.com", password="userpass")

        # аутентификация клиентов
        self.client_user = APIClient()
        self.client_user.force_authenticate(user=self.regular_user)

        self.other_user_client = APIClient()
        self.other_user_client.force_authenticate(user=self.other_user)

        self.habit = Habit.objects.create(user=self.regular_user, action="Habit 1", time="10:00", place="Home")
        self.url = reverse("habit:subscription-list")

    def test_subscribe_creates_subscription(self):
        response = self.client_user.post(self.url, {"habit": self.habit.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "подписка добавлена")
        self.assertTrue(Subscription.objects.filter(subscriber=self.regular_user, habit=self.habit).exists())

    def test_subscription_list_shows_only_user(self):
        sub1 = Subscription.objects.create(subscriber=self.regular_user, habit=self.habit)
        other_habit = Habit.objects.create(user=self.other_user, action="Other habit", time="09:00", place="Park")
        sub2 = Subscription.objects.create(subscriber=self.other_user, habit=other_habit)

        response = self.client_user.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], sub1.id)
        sub2.delete()
