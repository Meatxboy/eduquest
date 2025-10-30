.PHONY: up down backend bot frontend lint format

up:
	docker compose up --build

down:
	docker compose down --volumes

backend:
	uvicorn app.main:app --reload --app-dir backend/app

bot:
	uvicorn app.main:app --reload --port 8081 --app-dir bot/app

frontend:
	npm --prefix frontend install
	npm --prefix frontend run dev -- --host
