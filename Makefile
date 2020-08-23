up:
	docker-compose up -d
down:
	docker-compose down
build:
	docker-compose down
	docker-compose up -d --build
logs:
	docker-compose logs -f web
ps:
	docker-compose ps
makemigrations:
	docker-compose exec web python manage.py makemigrations
migrate:
	docker-compose exec web python manage.py migrate