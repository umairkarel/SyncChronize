"""Views"""

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from api.utils import check_user_availability
import api.serializers
import backend.models


class ScheduleViewSet(viewsets.ModelViewSet):
    """View for Schedule CRUD"""

    queryset = backend.models.Schedule.objects.all()

    def get_serializer_class(self):
        """Selecting the appropriate serializer based on the request method"""

        if self.action == "create" or self.action == "partial_update":
            return api.serializers.ScheduleCreateSerializer

        return api.serializers.ScheduleDetailSerializer

    def create(self, request, *args, **kwargs):
        unavailable_users = check_user_availability(request.data)

        if unavailable_users:
            return Response(
                {
                    "error": "There are conflicts in the schedule",
                    "unavailable_users": unavailable_users,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        op_serialize = api.serializers.ScheduleDetailSerializer(instance, many=False)
        return Response(
            {"message": "Successfully scheduled!", "data": op_serialize.data},
            status=status.HTTP_201_CREATED,
        )

    def perform_create(self, serializer):
        return serializer.save()

    def partial_update(
        self, request, pk=None, *args, **kwargs
    ):  # pylint: disable=W1113
        unavailable_users = check_user_availability(request.data)

        if unavailable_users:
            return Response(
                {
                    "error": "There are conflicts in the Schedule",
                    "unavailable_users": unavailable_users,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = get_object_or_404(backend.models.Schedule, pk=pk)
        updated = serializer.update(instance, serializer.data)
        op_serialize = api.serializers.ScheduleDetailSerializer(updated, many=False)
        return Response(
            {"message": "Successfully updated!", "data": op_serialize.data},
            status=status.HTTP_200_OK,
        )


class UserReadableViewset(
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """View for User CRUD"""

    queryset = User.objects.all()
    serializer_class = api.serializers.UserSerializer
