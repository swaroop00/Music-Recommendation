"""Background tasks for refreshing Spotify recommendations."""

from celery import shared_task
from django.utils import timezone
from django.core.cache import cache
from datetime import timedelta

from spotify.client import search_tracks
from users.models import UserProfile
from .models import Recommendation


@shared_task
def refresh_recommendations(user_id):
    """Build fresh Spotify recommendations for a single user."""
    user = UserProfile.objects.get(id=user_id)

    preferences = user.preferences or {}
    artists = preferences.get("artists", [])
    genres = preferences.get("genres", [])

    queries = []
    queries.extend(artists)
    queries.extend(genres)

    tracks = []
    for query in queries:
        result = search_tracks(query, 5)

        spotify_tracks = result.get("tracks", {}).get("items", [])

        for track in spotify_tracks:
            tracks.append({
                "id": track.get("id"),
                "name": track.get("name"),
                "artist": [
                    artist.get("name")
                    for artist in track.get("artists", [])
                ],
                "album": track.get("album", {}).get("name"),
                "spotify_url": (
                    track.get("external_urls", {}).get("spotify")
                ),
                "duration_ms": track.get("duration_ms"),
            })



    recommendation_data = {
        "user_id": user.id,
        "preferences": preferences,
        "tracks": tracks,
        "source": "spotify",
    }

    # recommendation_data = {
    #     "user_id": user.id,
    #     "preferences": preferences,
    #     "tracks": [],
    #     "source": "spotify",
    # }
    recommendation = Recommendation.objects.create(
        user=user,
        tracks=tracks,
        spotify_response=recommendation_data,
        expires_at=timezone.now() + timedelta(hours=1),
    )

    # Invalidate old cached recommendation
    cache_key = f"recommendations:user:{user_id}"
    cache.delete(cache_key)

    return {
        "recommendation_id": recommendation.id,
        "user_id": user.id,
    }

@shared_task
def refresh_all_recommendations():
    """Queue recommendation refresh tasks for every user."""
    users = UserProfile.objects.all()

    queued_users = 0

    for user in users:
        refresh_recommendations.delay(user.id)
        queued_users += 1

    return {
        "message": "Recommendation refresh tasks queued",
        "users_count": queued_users,
    }