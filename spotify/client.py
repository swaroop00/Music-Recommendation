import os
import requests
from dotenv import load_dotenv

load_dotenv()


def get_spotify_access_token():
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "client_credentials",
        },
        auth=(client_id, client_secret),
        timeout=10,
    )

    response.raise_for_status()

    return response.json()["access_token"]


def search_tracks(query, limit=10):
    token = get_spotify_access_token()

    response = requests.get(
        "https://api.spotify.com/v1/search",
        headers={
            "Authorization": f"Bearer {token}"
        },
        params={
            "q": query,
            "type": "track",
            "limit": limit,
            "market": "IN",
        },
        timeout=10,
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)

    response.raise_for_status()

    return response.json()