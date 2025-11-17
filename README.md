# EduQuest Mini App MVP

Минимальная версия геймифицированного трекера прогресса, состоящая из Telegram-бота, мини-приложения и python-бэкенда с PostgreSQL и Redis.

## Компоненты

- **Backend (`backend/`)** — FastAPI, PostgreSQL, Redis; отвечает за верификацию initData, выдаёт текущее состояние игрока и фиксирует прогресс.
- **Telegram Bot (`bot/`)** — aiogram 3; отдаёт кнопку запуска мини-приложения и обрабатывает webhook/polling.
- **Mini App (`frontend/`)** — React + Vite SPA, подключается к Telegram WebApp API и общается с бэкендом.
- **Инфраструктура** — `docker-compose.yml` с PostgreSQL, Redis, backend, bot и frontend, вспомогательные Makefile-таргеты.

## Быстрый старт

1. Скопируйте `.env.example` в `.env` в директориях `backend/`, `bot/`, `frontend/` и заполните значения.
2. Соберите и запустите стэк:
   ```bash
   docker compose up --build
   ```
3. Backend доступен на `http://localhost:8000`, фронтенд мини-приложение — `http://localhost:4173`.
4. Чтобы посмотреть Dev-режим без Telegram, откройте фронтенд и добавьте `?mockUser=1` к URL.

## Разработка локально

- Backend: `make backend` (uvicorn с авто-перезапуском, использует `.env`).
- Bot: `make bot` — запуск FastAPI вебхука или polling (если `WEBHOOK_URL` пустой).
- Frontend: `make frontend` — установка зависимостей и старт Vite dev-сервера.

## База данных и миграции

- При старте backend создаёт таблицы автоматически (`SQLAlchemy` metadata).
- Для первичных данных можно применить `infra/seed.sql` (например `psql < infra/seed.sql`).
- Alembic не настроен, но структура готова для интеграции.

## Проверка подписи Telegram

- `backend/app/utils/telegram.py` реализует верификацию initData HMAC.
- В режиме `ENVIRONMENT=development` допускается заглушка с `hash=dev` (для локального теста без Telegram).

## Наблюдаемость

- Логи — JSON через `structlog` в stdout для backend и бота.
- Метрики — `/metrics` через `prometheus-fastapi-instrumentator` на backend.
- Health-check — `GET /health` на backend и боте.
git clone https://github.com/Meatxboy/eduquest eduquest && cd eduquest
## Следующие шаги

- Добавить настоящие миграции (Alembic) и seed-скрипты.
- Настроить auth/ACL для мини-приложения (подпись запросов на backend).
- Доработать игровую механику: урон, уровни, награды и историю выполнения.
- Подключить real-time обновления (websocket/long polling) и уведомления через бота.
