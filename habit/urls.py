from rest_framework.routers import DefaultRouter

from habit.apps import HabitConfig
from habit.views import HabitViewSet, PublicHabitsViewSet, SubscriptionViewSet

app_name = HabitConfig.name

router = DefaultRouter()
router.register(r"habits", HabitViewSet, basename="user_habits")
router.register(r"public_habits", PublicHabitsViewSet, basename="public_habits")
router.register(r'subscriptions', SubscriptionViewSet, basename='subscription')

urlpatterns = router.urls
