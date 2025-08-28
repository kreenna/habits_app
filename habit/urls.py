from rest_framework.routers import DefaultRouter

from habit.apps import HabitConfig
from habit.views import HabitViewSet, PublicHabitsViewSet

app_name = HabitConfig.name

router = DefaultRouter()
router.register(r"habits", HabitViewSet, basename="user_habits")
router.register(r"public_habits", PublicHabitsViewSet, basename="public_habits")

urlpatterns = router.urls
