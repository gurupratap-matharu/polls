up:
	docker-compose up -d
down:
	docker-compose down
build:
	docker-compose down
	docker-compose up -d --build
logs:
	docker-compose exec web logs -f
ps:
	docker-compose ps