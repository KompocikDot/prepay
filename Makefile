up:
	docker compose up

up-d:
	docker compose up -d

build:
	docker compose build

db-migrate:
	docker compose exec -it django python manage.py migrate

db-makemigrations:
	docker compose exec -it django python manage.py makemigrations

createsu:
	docker compose exec -it django python manage.py createsuperuser

makemessages:
	docker compose exec -it django python manage.py makemessages -l pl

sh:
	docker compose exec -it django sh
