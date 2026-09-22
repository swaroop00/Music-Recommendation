# Music Recommendation

A scalable backend service for personalized music recommendations using Django REST Framework, PostgreSQL, Redis, Celery, Docker, and the Spotify Web API.

## Features

- User profile management
- Music preferences including:
  - Favorite genres
  - Favorite artists
  - Moods
- Spotify track search and recommendation generation
- Asynchronous recommendation refresh using Celery
- Periodic recommendation refresh using Celery Beat
- Redis-based recommendation caching
- PostgreSQL persistence
- User activity tracking:
  - Play
  - Like
  - Skip
- Analytics APIs
- Dockerized development environment
- Nginx reverse proxy
- RESTful APIs using Django REST Framework

---

## Tech Stack

- Python 3.12
- Django
- Django REST Framework
- PostgreSQL
- Redis
- Celery
- Celery Beat
- Spotify Web API
- Docker & Docker Compose
- Nginx

---

## Architecture

```text
Client
  |
  v
Nginx
  |
  v
Django REST API
  |
  +---- PostgreSQL
  |
  +---- Redis
  |
  +---- Celery ----> Spotify API
```

---

## Project Structure

```text
Music Recommendation/
│
├── activities/
├── analytics/
├── music_discovery/
├── recommendations/
├── users/
├── spotify/
├── nginx/
│
├── postman/
│   └── music-recommendation.postman_collection.json
│
├── .env
├── .env.example
├── .dockerignore
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── manage.py
├── README.md
└── requirements.txt
```

---

## Setup

### 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd "Music Recommendation"
```

### 2. Create Environment File

Create a `.env` file in the project root.

```env
DB_NAME=music_discovery_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

REDIS_HOST=localhost

SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
```

Do not commit the `.env` file to GitHub.

The project includes an `.env.example` file with placeholder values.

---

## Running with Docker

Make sure Docker Desktop is installed and running.

Build and start all services:

```bash
docker compose up --build
```

The application uses the following services:

- Django
- PostgreSQL
- Redis
- Celery Worker
- Celery Beat
- Nginx

### API

Through Nginx:

```text
http://localhost/api/
```

Direct Django server:

```text
http://localhost:8000/api/
```

---

## Database Migrations

Run migrations:

```bash
docker compose exec web python manage.py migrate
```

Create migrations after model changes:

```bash
docker compose exec web python manage.py makemigrations
```

---

## API Endpoints

### Users

#### Create / Update User

```http
POST /api/users/
```

Example request:

```json
{
  "name": "Swaroop",
  "email": "swaroop@test.com",
  "preferences": {
    "genres": ["pop", "rock"],
    "artists": ["Coldplay"],
    "moods": ["happy", "energetic"]
  }
}
```

#### Get Users

```http
GET /api/users/
```

#### Get User

```http
GET /api/users/{user_id}/
```

---

### Recommendations

#### Refresh Recommendations

```http
POST /api/recommendations/{user_id}/refresh/
```

The request queues a background Celery task.

Example response:

```json
{
  "message": "Recommendation refresh task queued",
  "user_id": "1"
}
```

#### Get Recommendations

```http
GET /api/recommendations/{user_id}/
```

The API checks Redis cache first. If cached data is unavailable, it retrieves the latest recommendation from PostgreSQL and stores it in Redis.

---

### User Activity

#### Create Activity

```http
POST /api/activity/
```

Supported actions:

- `play`
- `like`
- `skip`

Example:

```json
{
  "user": 1,
  "track_id": "3RiPr603aXAoi4GHyXx0uy",
  "action": "play"
}
```

#### Get Activities

```http
GET /api/activity/
```

---

### Analytics

#### Summary

```http
GET /api/analytics/summary/
```

Returns:

- Total users
- Total activities
- Total plays
- Total likes
- Total skips

#### Trends

```http
GET /api/analytics/trends/
```

Returns aggregated activity trends.

#### User Analytics

```http
GET /api/analytics/user/{user_id}/
```

Returns:

- Total activities
- Plays
- Likes
- Skips
- Engagement rate

Example:

```json
{
  "user_id": 1,
  "user": "Swaroop",
  "total_activities": 3,
  "total_plays": 1,
  "total_likes": 1,
  "total_skips": 1,
  "engagement_rate": 66.67
}
```

---

## Spotify Integration

The application integrates with the Spotify Web API to search for tracks based on user preferences.

The recommendation process currently uses:

- Favorite artists
- Favorite genres

Spotify Client Credentials flow is used for server-to-server API access.

Spotify credentials must be configured in `.env`.

---

## Recommendation Flow

```text
User Profile
     |
     v
User Preferences
     |
     v
Refresh Recommendation API
     |
     v
Celery Task
     |
     v
Spotify Web API
     |
     v
Track Results
     |
     +-------------------+
     |                   |
     v                   v
PostgreSQL             Redis
     |                   |
     +---------+---------+
               |
               v
      Recommendation API
```

---

## Celery

Celery is used for asynchronous recommendation processing.

Start the Celery worker:

```bash
docker compose exec celery celery -A music_discovery worker --loglevel=info --pool=solo
```

Celery Beat is used for periodic recommendation refresh.

The current schedule refreshes recommendations every hour.

---

## Redis Caching

Recommendation responses are cached in Redis.

Cache key format:

```text
recommendations:user:{user_id}
```

Cache duration:

```text
3600 seconds
```

When a new recommendation is generated, the existing cache entry for that user is invalidated.

---

## PostgreSQL Persistence

PostgreSQL stores:

- User profiles
- User preferences
- Recommendation records
- Spotify response data
- User activity records

---

## Nginx

Nginx acts as a reverse proxy in front of Django.

```text
Client
  |
  v
Nginx :80
  |
  v
Django :8000
```

Example:

```text
http://localhost/api/users/
```

---

## Docker Services

| Service | Purpose |
|---|---|
| `web` | Django REST API |
| `db` | PostgreSQL database |
| `redis` | Redis cache and Celery broker |
| `celery` | Background task worker |
| `celery-beat` | Periodic task scheduler |
| `nginx` | Reverse proxy |

---

## Testing

The project includes automated API tests using Django REST Framework.

Run all tests:

```bash
docker compose exec web python manage.py test
```

Current test coverage includes:

- User APIs
- Recommendation APIs
- Activity APIs
- Analytics APIs

Current test suite:

```text
9 tests
All tests passing
```

---

## Postman Collection

A Postman collection is included for testing the API endpoints.

Collection file:

```text
postman/music-recommendation.postman_collection.json
```

Import this file into Postman to test:

- User APIs
- Recommendation APIs
- Activity APIs
- Analytics APIs

The collection uses the following variable:

```text
{{base_url}}
```

Default value:

```text
http://localhost
```

The `user_id` variable is also included for user-specific endpoints.

---

## Makefile

Common Docker commands are available through the Makefile.

```bash
make up
```

Start the application.

```bash
make down
```

Stop the application.

```bash
make migrate
```

Run database migrations.

```bash
make makemigrations
```

Create migrations.

```bash
make test
```

Run the test suite.

```bash
make logs
```

View Django logs.

```bash
make celery-logs
```

View Celery logs.

---

## Useful Docker Commands

### Start services

```bash
docker compose up
```

### Build containers

```bash
docker compose up --build
```

### Stop services

```bash
docker compose down
```

### View running containers

```bash
docker compose ps
```

### View Django logs

```bash
docker compose logs web
```

### View Celery logs

```bash
docker compose logs celery
```

### View Celery Beat logs

```bash
docker compose logs celery-beat
```

### Open Django shell

```bash
docker compose exec web python manage.py shell
```

---

## Environment Variables

| Variable | Description |
|---|---|
| `DB_NAME` | PostgreSQL database name |
| `DB_USER` | PostgreSQL username |
| `DB_PASSWORD` | PostgreSQL password |
| `DB_HOST` | PostgreSQL host |
| `DB_PORT` | PostgreSQL port |
| `REDIS_HOST` | Redis host |
| `SPOTIFY_CLIENT_ID` | Spotify application client ID |
| `SPOTIFY_CLIENT_SECRET` | Spotify application client secret |

---

## Security

- Secrets are stored in `.env`.
- `.env` is excluded from the Docker build context.
- `.env` should not be committed to GitHub.
- `.env.example` contains placeholder values only.

---

## Future Improvements

Possible improvements include:

- API rate limiting
- Additional automated test coverage
- Spotify access-token caching
- Retry handling for Spotify API failures
- Track deduplication
- Recommendation expiry validation
- Health-check endpoints
- Production WSGI server configuration
- CI/CD pipeline

---

## Author

Swaroop Thomare

Backend Developer  
Python | Django | Django REST Framework | PostgreSQL | Redis | Celery