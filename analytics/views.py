from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from django.db import models

from users.models import UserProfile
from activities.models import UserActivity


class AnalyticsSummaryView(APIView):

    def get(self, request):
        total_users = UserProfile.objects.count()
        total_activities = UserActivity.objects.count()

        activity_counts = UserActivity.objects.aggregate(
            total_plays=Count("id", filter=models.Q(action="play")),
            total_likes=Count("id", filter=models.Q(action="like")),
            total_skips=Count("id", filter=models.Q(action="skip")),
        )

        return Response(
            {
                "total_users": total_users,
                "total_activities": total_activities,
                "total_plays": activity_counts["total_plays"],
                "total_likes": activity_counts["total_likes"],
                "total_skips": activity_counts["total_skips"],
            },
            status=status.HTTP_200_OK,
        )

class AnalyticsTrendsView(APIView):

    def get(self, request):
        trending_actions = (
            UserActivity.objects
            .values("action")
            .annotate(total=Count("id"))
            .order_by("-total")
        )

        return Response(
            {
                "trending_actions": trending_actions
            },
            status=status.HTTP_200_OK,
        )


class UserAnalyticsView(APIView):

    def get(self, request, user_id):
        try:
            user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response(
                {
                    "message": "User not found",
                    "user_id": user_id
                },
                status=status.HTTP_404_NOT_FOUND
            )

        activities = UserActivity.objects.filter(user=user)

        counts = activities.aggregate(
            total_plays=Count(
                "id",
                filter=models.Q(action="play")
            ),
            total_likes=Count(
                "id",
                filter=models.Q(action="like")
            ),
            total_skips=Count(
                "id",
                filter=models.Q(action="skip")
            ),
        )

        total_activities = activities.count()

        engagement_rate = 0

        if total_activities > 0:
            engagement_rate = round(
                (
                    counts["total_likes"] + counts["total_plays"]
                ) / total_activities * 100,
                2
            )

        return Response(
            {
                "user_id": user.id,
                "user": user.name,
                "total_activities": total_activities,
                "total_plays": counts["total_plays"],
                "total_likes": counts["total_likes"],
                "total_skips": counts["total_skips"],
                "engagement_rate": engagement_rate
            },
            status=status.HTTP_200_OK
        )