"""URL Patterns for API"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
import api.views


router = DefaultRouter()

router.register(r"schedule", api.views.ScheduleViewSet, basename="schedule")
router.register(r"user", api.views.UserReadableViewset, basename="user")

urlpatterns = [
    path("api-auth", include("rest_framework.urls", namespace="rest_framework")),
    path("", include(router.urls)),
]
