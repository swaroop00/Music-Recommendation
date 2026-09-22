from rest_framework.test import APITestCase
from rest_framework import status


class UserAPITestCase(APITestCase):

    def test_create_user(self):
        data = {
            "name": "Test User",
            "email": "testuser@example.com",
            "preferences": {
                "genres": ["pop"],
                "artists": ["Coldplay"],
                "moods": ["happy"]
            }
        }

        response = self.client.post(
            "/api/users/",
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.data["name"],
            "Test User"
        )

        self.assertEqual(
            response.data["email"],
            "testuser@example.com"
        )

    def test_get_users(self):
        response = self.client.get("/api/users/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )