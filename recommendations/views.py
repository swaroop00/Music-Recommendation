"""API views for recommendation retrieval and refresh actions."""

from django.db.migrations import serializer
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import action
from .models import Recommendation
from .serializers import RecommendationSerializer
from rest_framework.response import Response
from .tasks import refresh_recommendations
from django.core.cache import cache

class RecommendationViewSet(viewsets.ModelViewSet):
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer
    @action(
        detail=False,
        methods=["get"],
        url_path=r"(?P<user_id>\d+)"
    )
    def user_recommendations(self, request, user_id=None):
        """Fetch a user's latest recommendation from cache or database."""
        cache_key = f"recommendations:user:{user_id}"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(
                {
                    "source": "cache",
                    "data": cached_data
                },
                status=status.HTTP_200_OK
            )


        recommendation = (
            Recommendation.objects
            .filter(user_id=user_id)
            .order_by("-created_at")
            .first()
        )

        if not recommendation:
            return Response(
                {
                    "message": "No recommendations found for this user",
                    "user_id": user_id
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(recommendation)

        cache.set(
            cache_key,
            serializer.data,
            3600  
        )  # Cache for 1 hour
        return Response(
            {
                "source": "database",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

    @action(
        detail=False,
        methods=["post"],
        url_path=r"(?P<user_id>\d+)/refresh"
    )
    def refresh(self, request, user_id=None):
        """Queue a background refresh for the user's recommendations."""
        refresh_recommendations.delay(user_id)

        return Response(
        {
            "message": "Recommendation refresh task queued",
            "user_id": user_id
        },
        status=status.HTTP_202_ACCEPTED
        )