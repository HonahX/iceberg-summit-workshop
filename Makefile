start:
	docker compose kill
	docker compose rm -f
	docker compose up

stop:
	docker compose down

rebuild:
	docker compose kill
	docker compose rm -f
	docker compose build --no-cache