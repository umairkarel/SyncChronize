"""Schema (Models)"""

from django.db import models
from django.contrib.auth.models import User
from backend.validators import validate_datetime


# Schedule Model/Table
class Schedule(models.Model):
    """Scheduler Model"""

    start_date_time = models.DateTimeField(
        blank=False, null=False, validators=[validate_datetime]
    )
    end_date_time = models.DateTimeField(
        blank=False, null=False, validators=[validate_datetime]
    )

    title = models.CharField(max_length=100, blank=False, null=False)
    users = models.ManyToManyField(User, related_name="scheduled_events", blank=False)

    def __str__(self):
        return f"{self.title}"


class UserAvailibility(User):
    """Proxying Django User Model to check if the user is available at the provided date and time"""

    class Meta:
        """Meta Properties"""

        proxy = True

    def user_not_available(self, start_date_time, end_date_time):
        """Returns the email of the user who has a schedule time conflicts.

        Args:
            start_date_time (datetime): start date and time for the event
            end_date_time (datetime): end date and time for the event
        """
        users_scheduled_events = self.scheduled_events.filter(
            start_date_time__lte=end_date_time, end_date_time__gte=start_date_time
        )

        # print(" \n\n >> USER >> : ", self.__dict__)
        # print(" \n\n >> USER EVENTS >> : ", users_scheduled_events)
        if users_scheduled_events:
            return self.email
