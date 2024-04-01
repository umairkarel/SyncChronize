"""Serializers for the Models"""

from rest_framework import serializers
from backend import models


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""

    class Meta:
        """Meta properties for UserSerializer."""

        model = models.User
        fields = ("id", "username", "email")


class UserSchedulerCreate(serializers.ModelSerializer):
    """Serializer for creating a User scheduler."""

    class Meta:
        """Meta properties for UserSchedulerCreate."""

        model = models.User
        fields = ("id",)


class ScheduleDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed representation of a Schedule model."""

    users = UserSerializer(many=True)

    class Meta:
        """Meta properties for ScheduleDetailSerializer."""

        model = models.Schedule
        fields = "__all__"


class ScheduleCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a Schedule model."""

    class Meta:
        """Meta properties for ScheduleCreateSerializer."""

        model = models.Schedule
        fields = "__all__"
