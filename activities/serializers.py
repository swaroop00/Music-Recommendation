"""Serializers for user activity API data."""

from rest_framework import serializers
from .models import UserActivity


class UserActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = UserActivity
        fields = [
            "id",
            "user",
            "track_id",
            "action",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
        ]