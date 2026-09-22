from rest_framework.test import APITestCase
from rest_framework import status

from users.models import UserProfile
from activities.models import UserActivity


class ActivityAPITestCase(APITestCase):

    def setUp(self):
        self.user = UserProfile.objects.create(
            name="Test User",
            email="activity@test.com",
            preferences={
                "genres": ["pop"],
                "artists": ["Coldplay"],
                "moods": ["happy"]
            }
        )

    def test_create_activity(self):
        data = {
            "user": self.user.id,
            "track_id": "3RiPr603aXAoi4GHyXx0uy",
            "action": "play"
        }

        response = self.client.post(
            "/api/activity/",
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.data["action"],
            "play"
        )

    def test_get_activities(self):
        UserActivity.objects.create(
            user=self.user,
            track_id="3AJwUDP919kvQ9QcozQPxg",
            action="like"
        )

        response = self.client.get("/api/activity/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )