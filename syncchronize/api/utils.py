"""Utility Functions"""

from datetime import datetime
from django.utils.timezone import make_aware
from backend.models import UserAvailibility


def clean_list(x):
    """
    Function to clean a list by removing None values.

    Parameters:
    x (list): The input list.

    Returns:
    list: The cleaned list without None values.
    """
    return x is not None


def user_availability(x, new_event_start, new_event_end):
    """
    Function to check user availability based on their id, start date, and end date.

    Parameters:
    x (int): The id of the user.
    new_event_start (datetime): The start date and time of the new event.
    new_event_end (datetime): The end date and time of the new event.

    Returns:
    bool: True if the user is not available during the specified time range, False otherwise.
    """
    user_availability_obj = UserAvailibility.objects.get(id=x)
    return user_availability_obj.userNotAvailable(
        start_date_time=new_event_start, end_date_time=new_event_end
    )


def check_user_availability(data):
    """
    Check the availability of users for a given event.

    Parameters:
    data (dict): A dictionary containing the event data, including 'users', 'start_date_time', and 'end_date_time'.

    Returns:
    list: A list of users who are not available during the specified time range.
    """
    added_users = data["users"]
    new_event_start = data["start_date_time"]
    new_event_end = data["end_date_time"]

    # Convert string dates to datetime objects
    new_event_start = make_aware(
        datetime.strptime(new_event_start, "%Y-%m-%dT%H:%M:%SZ")
    )
    new_event_end = make_aware(datetime.strptime(new_event_end, "%Y-%m-%dT%H:%M:%SZ"))

    # Check availability for each user
    unavailable_users = list(
        map(
            lambda user_id: user_availability(user_id, new_event_start, new_event_end),
            added_users,
        )
    )

    # Filter out None values from the result
    unavailable_users = list(filter(clean_list, unavailable_users))

    return unavailable_users
