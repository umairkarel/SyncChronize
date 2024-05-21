"""Data Validators"""

import datetime
from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_datetime(value: datetime.datetime):
    """A field validater for determinig if the date entered is a future date or not
    (Only allows future dates)

    Args:
        value (datetime.datetime): datetime to check validity

    Raises:
        ValidationError: invalid datetime passed

    Returns:
        datetime.datetime: value if valid
    """
    if value < (
        timezone.now() - datetime.timedelta(seconds=2)
    ):  # Compensating 2 seconds for network or user-action latency
        raise ValidationError("You can not schedule an event for the past!")
    return value
