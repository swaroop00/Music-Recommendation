"""Serializers for recommendation objects and responses."""

from rest_framework import serializers
from .models import Recommendation

class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = ['id', 'user', 'tracks', 'spotify_response', 'created_at', 'expires_at']
        read_only_fields = [
            "id",
            "created_at",
        ]