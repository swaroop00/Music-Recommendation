up:
	docker compose up --build

down:
	docker compose down

migrate:
	docker compose exec web python manage.py migrate

makemigrations:
	docker compose exec web python manage.py makemigrations

test:
	docker compose exec web python manage.py test

logs:
	docker compose logs -f web

celery-logs:
	docker compose logs -f celery