from rest_framework.test import APITestCase
from rest_framework import status

from users.models import UserProfile
from activities.models import UserActivity


class AnalyticsAPITestCase(APITestCase):

    def setUp(self):
        self.user = UserProfile.objects.create(
            name="Analytics User",
            email="analytics@test.com",
            preferences={
                "genres": ["pop"],
                "artists": ["Coldplay"],
                "moods": ["happy"]
            }
        )

        UserActivity.objects.create(
            user=self.user,
            track_id="track1",
            action="play"
        )

        UserActivity.objects.create(
            user=self.user,
            track_id="track2",
            action="like"
        )

        UserActivity.objects.create(
            user=self.user,
            track_id="track3",
            action="skip"
        )

    def test_summary(self):
        response = self.client.get(
            "/api/analytics/summary/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_trends(self):
        response = self.client.get(
            "/api/analytics/trends/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_user_analytics(self):
        response = self.client.get(
            f"/api/analytics/user/{self.user.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["total_activities"],
            3
        )

        self.assertEqual(
            response.data["total_plays"],
            1
        )

        self.assertEqual(
            response.data["total_likes"],
            1
        )

        self.assertEqual(
            response.data["total_skips"],
            1
        )