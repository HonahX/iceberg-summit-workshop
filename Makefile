start:
	docker compose kill
	docker compose rm -f
	docker compose up -d

stop:
	docker compose down

rebuild:
	docker compose kill
	docker compose rm -f
	docker compose build --no-cache

setup:
	docker compose kill
	docker compose rm -f
	docker compose build --no-cache
	docker compose up -d
	docker compose down