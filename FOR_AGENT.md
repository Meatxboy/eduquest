# EduQuest Mini App — Overview

EduQuest is an MVP of a gamified learning tracker that consists of:

- **Backend (FastAPI, async SQLAlchemy)** — verifies Telegram WebApp `initData`, stores users/tasks/goals in PostgreSQL, exposes state/update endpoints, and publishes Prometheus metrics.
- **Telegram Bot (aiogram 3 + FastAPI)** — provides a WebApp button, optional webhook endpoint, and health check. Supports polling fallback for local dev.
- **Mini App Frontend (React + Vite SPA)** — consumes Telegram WebApp API, shows a single current task, daily goals, health/progress bars, and completes tasks via REST.
- **Data layer** — PostgreSQL 15 + Redis 7 (cache/session placeholder). Simple SQL seed script for starter tasks.
- **Observability** — JSON logs via structlog, `/metrics` via `prometheus-fastapi-instrumentator`, `/health` endpoints for bot/back.
- **Infrastructure** — Docker Compose stack, service-specific `.env` files, nginx reverse proxy + Certbot for single-domain HTTPS deployment.

Key flows:
1. Telegram bot opens `initData`; frontend sends it to backend `/api/v1/auth/init`.
2. Backend validates signature, ensures user/tasks/goals, returns `UserState`.
3. Mini app completes current task via `/api/v1/state/tasks/complete` and re-renders state.
4. Redis reserved for future caching/session data; currently only backend closes client on shutdown.

Dev conveniences:
- `?mockUser=1` query uses a stub `initData` when `ENVIRONMENT=development`.
- Make targets (`backend`, `bot`, `frontend`) run services locally.
- Dockerfiles for backend/bot/frontend support containerized builds.
