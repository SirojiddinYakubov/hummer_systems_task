#!/usr/bin/make

include deploy/.env.dev

help:
	@echo "make"
	@echo "	hello"
	@echo "		print hello world"

hello:
	echo "Hello, World"
run:
	python manage.py runserver $(SVC_PORT)
docker-build:
	docker compose -f deploy/docker-compose-prod.yml --env-file=deploy/.env.prod build
docker-down:
	docker compose -f deploy/docker-compose-prod.yml --env-file=deploy/.env.prod down
docker-up:
	docker compose -f deploy/docker-compose-prod.yml --env-file=deploy/.env.prod up -d --build