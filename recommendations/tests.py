from rest_framework.test import APITestCase
from rest_framework import status

from users.models import UserProfile
from recommendations.models import Recommendation


class RecommendationAPITestCase(APITestCase):

    def setUp(self):
        self.user = UserProfile.objects.create(
            name="Test User",
            email="recommendation@test.com",
            preferences={
                "genres": ["pop"],
                "artists": ["Coldplay"],
                "moods": ["happy"]
            }
        )

        self.recommendation = Recommendation.objects.create(
            user=self.user,
            tracks=[
                {
                    "id": "test123",
                    "name": "Test Song",
                    "artist": ["Test Artist"]
                }
            ],
            spotify_response={
                "source": "spotify"
            }
        )

    def test_get_user_recommendations(self):
        response = self.client.get(
            f"/api/recommendations/{self.user.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertIn(
            "data",
            response.data
        )

    def test_refresh_recommendations(self):
        response = self.client.post(
            f"/api/recommendations/{self.user.id}/refresh/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_202_ACCEPTED
        )

        self.assertEqual(
            response.data["user_id"],
            str(self.user.id)
        )