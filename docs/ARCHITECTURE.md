# Архитектура EduQuest MVP

## Общая схема

```
Telegram <-webhook-> Bot (aiogram/FastAPI) <-REST-> Backend (FastAPI)
                                 |                         |
                               Mini App (React) <--HTTP-->|
                                 |                         |
                             Browser (Telegram WebView)    |
                                                           |
                                                                   PostgreSQL + Redis
```

- **Bot** — отвечает за пользовательский вход, отдаёт WebApp-кнопку, проксирует события (при необходимости) и может посылать пуши.
- **Backend** — единая точка бизнес-логики: верифицирует `initData`, хранит пользователей, задачи и цели.
- **Mini App** — отображает состояние игрока, вызывает REST-методы бэкенда, использует Telegram WebApp API.
- **PostgreSQL** — хранит пользователей, задачи, цели и прогресс.
- **Redis** — кэш/подготовка к хранению сессий и метаданных (задача на будущее).

## Поток запуска мини-приложения

1. Пользователь нажимает кнопку в чате → Telegram открывает WebApp и передаёт `initData`.
2. Фронтенд отправляет `initData` на `/api/v1/auth/init`.
3. Backend проверяет подпись, создаёт пользователя и выдаёт текущее состояние (здоровье, прогресс, текущая задача, цели).
4. Пользователь выполняет задачу → фронтенд вызывает `/api/v1/state/tasks/complete`.
5. Backend обновляет прогресс, возвращает новое состояние и фронтенд обновляет UI.

## Модели данных

- `User` — telegram_id, username, level, experience, health_points, attributes (JSON), связи с задачами и целями.
- `Task` — справочник задач (title, description, difficulty, xp_reward, health_delta).
- `UserTask` — очередь задач конкретного пользователя, хранит статус и порядок выполнения.
- `DailyGoal` — цели на вчера/сегодня/завтра.

## API кратко

- `POST /api/v1/auth/init` — принимает `init_data`, возвращает `UserState`.
- `GET /api/v1/state` — состояние пользователя по `telegram_id`.
- `POST /api/v1/state/tasks/complete` — завершить задачу, ответ — новое состояние.
- `GET /health` — health-check.

## Наблюдаемость

- JSON-логи в stdout (готово для сбора log-агентом).
- `/metrics` с Prometheus-инструментатором.
- Возможность расширить трассировку (например, OpenTelemetry) — задел в структуре проекта.

## Безопасность

- Верификация Telegram `initData` (prod).
- Dev-режим разрешает заглушку с `hash=dev`.
- Запросы на изменение состояния требуют указания `telegram_id` и проходят через `ensure_user` (дополнительно можно ввести токенизацию).
