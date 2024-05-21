"""Tests"""

import datetime
import pandas as pd
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase
import backend.models


print("\n\n+++++++++++++++++ Initiating API Test +++++++++++++++++\n\n")


class Schedule(APITestCase):
    """Tests for Schedule"""

    def test_create_schedule(self):
        """
        This test ensures that we can create a schedule
        """

        # The following dict maps the values from the csv test cases to prapare the payload
        mapping = {
            "None": None,
            "Schedule": "song",
            "Not None": "Stand UP - Product Discussion",
        }

        # Reading test cases and untitest from csv
        df_test_cases = pd.read_csv("unittest_data/SCHEDULE_API_TEST_CASES.csv")
        df_test_cases = df_test_cases[df_test_cases["Method"] == "create_schedule"]

        print("\n Testing create_schedule ...")

        for _, row in df_test_cases.iterrows():
            with self.subTest(params=row):
                # Pre-cleanup
                backend.models.Schedule.objects.all().delete()
                User.objects.all().delete()
                if row["startTime"].lower() == "future":
                    start_date_time = (
                        timezone.now() + datetime.timedelta(seconds=50)
                    ).strftime("%Y-%m-%dT%H:%M:%SZ")
                else:
                    start_date_time = (
                        timezone.now() - datetime.timedelta(seconds=50)
                    ).strftime("%Y-%m-%dT%H:%M:%SZ")

                if row["endTime"].lower() == "future":
                    end_date_time = (
                        timezone.now() + datetime.timedelta(seconds=50)
                    ).strftime("%Y-%m-%dT%H:%M:%SZ")
                else:
                    end_date_time = (
                        timezone.now() - datetime.timedelta(seconds=50)
                    ).strftime("%Y-%m-%dT%H:%M:%SZ")

                if row["users"].lower() == "available":
                    user = User.objects.create_user(
                        username="john", email="jdoe@abc.com", password="something123"
                    )
                else:
                    user = User.objects.create_user(
                        username="john", email="jdoe@abc.com", password="something123"
                    )
                    schedule = backend.models.Schedule.objects.create(
                        title="Important Meeting",
                        start_date_time=start_date_time,
                        end_date_time=end_date_time,
                    )
                    schedule.users.add(user)

                # preparing payload for testing API
                payload = {
                    "title": mapping[row["title"]],
                    "users": [user.id],
                    "start_date_time": start_date_time,
                    "end_date_time": end_date_time,
                }

                url = reverse("schedule-list")

                response = self.client.post(
                    url,
                    headers={"Content-Type": "application/json"},
                    data=payload,
                    format="json",
                )

                self.assertEqual(
                    response.status_code,
                    row["Expected"],
                    msg={
                        "url": url,
                        "request_payload": payload,
                        "response": response.json(),
                    },
                )

    def test_retrieve_schedule(self):
        """
        This test ensures that we can retrieve the details of a particular schedule
        """
        print("\n Testing retrieve_schedule ...")
        user1 = User.objects.create_user(
            username="john1", email="jdoe@abc.com", password="something123"
        )
        user2 = User.objects.create_user(
            username="john2", email="jdow@def.com", password="something123"
        )

        start_date_time = (timezone.now() + datetime.timedelta(seconds=50)).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )
        end_date_time = (timezone.now() + datetime.timedelta(seconds=50)).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )

        schedule = backend.models.Schedule.objects.create(
            title="Important Meeting",
            start_date_time=start_date_time,
            end_date_time=end_date_time,
        )
        schedule.users.add(user1)
        schedule.users.add(user2)

        url = reverse("schedule-detail", kwargs={"pk": schedule.id})

        response = self.client.get(url)
        self.assertEqual(
            response.status_code, 200, msg={"url": url, "response": response.json()}
        )

    def test_list_schedule(self):
        """
        This test ensures that we can list all Schedules
        """
        print("\n Testing list_schedule ...")

        user1 = User.objects.create_user(
            username="john1", email="jdoe@abc.com", password="something123"
        )
        user2 = User.objects.create_user(
            username="john2", email="jdow@def.com", password="something123"
        )

        start_date_time = (timezone.now() + datetime.timedelta(seconds=50)).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )
        end_date_time = (timezone.now() + datetime.timedelta(seconds=50)).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )

        schedule1 = backend.models.Schedule.objects.create(
            title="Important Meeting",
            start_date_time=start_date_time,
            end_date_time=end_date_time,
        )
        schedule1.users.add(user1)

        schedule2 = backend.models.Schedule.objects.create(
            title="Important Meeting",
            start_date_time=start_date_time,
            end_date_time=end_date_time,
        )

        schedule2.users.add(user2)

        url = reverse("schedule-list")

        response = self.client.get(url)
        self.assertEqual(
            response.status_code, 200, msg={"url": url, "response": response.json()}
        )

    def test_update_schedule(self):
        """
        This test ensures that we can update an existing schedule object
        """

        # The following dict maps the values from the csv test cases to prapare the payload
        mapping = {
            "None": None,
            "Schedule": "song",
            "Not None": "Stand UP - Product Discussion",
        }

        # Reading test cases and untitest from csv
        df_test_cases = pd.read_csv("unittest_data/SCHEDULE_API_TEST_CASES.csv")
        df_test_cases = df_test_cases[df_test_cases["Method"] == "update_schedule"]

        print("\n Testing update_schedule ...")

        for _, row in df_test_cases.iterrows():
            with self.subTest(params=row):

                # Pre-cleanup
                backend.models.Schedule.objects.all().delete()
                User.objects.all().delete()

                if row["startTime"].lower() == "future":
                    start_date_time = (
                        timezone.now() + datetime.timedelta(seconds=50)
                    ).strftime("%Y-%m-%dT%H:%M:%SZ")
                else:
                    start_date_time = (
                        timezone.now() - datetime.timedelta(seconds=50)
                    ).strftime("%Y-%m-%dT%H:%M:%SZ")

                if row["endTime"].lower() == "future":
                    end_date_time = (
                        timezone.now() + datetime.timedelta(seconds=50)
                    ).strftime("%Y-%m-%dT%H:%M:%SZ")
                else:
                    end_date_time = (
                        timezone.now() - datetime.timedelta(seconds=50)
                    ).strftime("%Y-%m-%dT%H:%M:%SZ")

                if row["users"].lower() == "available":
                    user = User.objects.create_user(
                        username="john", email="jdoe@abc.com", password="something123"
                    )
                else:
                    user = User.objects.create_user(
                        username="john", email="jdoe@abc.com", password="something123"
                    )
                    schedule = backend.models.Schedule.objects.create(
                        title="Important Meeting",
                        start_date_time=start_date_time,
                        end_date_time=end_date_time,
                    )
                    schedule.users.add(user)

                schedule_main = backend.models.Schedule.objects.create(
                    title="Some Important Meeting",
                    start_date_time=start_date_time,
                    end_date_time=end_date_time,
                )

                # preparing payload for testing API
                payload = {
                    "title": mapping[row["title"]],
                    "users": [user.id],
                    "start_date_time": start_date_time,
                    "end_date_time": end_date_time,
                }

                url = reverse("schedule-detail", kwargs={"pk": schedule_main.id})

                response = self.client.patch(
                    url,
                    headers={"Content-Type": "application/json"},
                    data=payload,
                    format="json",
                )
                self.assertEqual(
                    response.status_code,
                    row["Expected"],
                    msg={
                        "url": url,
                        "request_payload": payload,
                        "response": response.json(),
                    },
                )

    def test_delete_schedule(self):
        """
        This test ensures that we can delete a schedule object
        """

        print("\n Testing delete_schedule ...")

        user = User.objects.create_user(
            username="john", email="jdoe@abc.com", password="something123"
        )

        start_date_time = (timezone.now() + datetime.timedelta(seconds=50)).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )
        end_date_time = (timezone.now() + datetime.timedelta(seconds=50)).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )

        schedule = backend.models.Schedule.objects.create(
            title="Important Meeting",
            start_date_time=start_date_time,
            end_date_time=end_date_time,
        )
        schedule.users.add(user)

        url = reverse("schedule-detail", kwargs={"pk": schedule.id})

        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, 204, msg={"url": url, "response": response}
        )
