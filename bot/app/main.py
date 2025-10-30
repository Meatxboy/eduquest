from __future__ import annotations

import asyncio
import logging
from contextlib import asynccontextmanager, suppress

from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramUnauthorizedError
from aiogram.types import Update
from fastapi import FastAPI, HTTPException, Request
from starlette.responses import JSONResponse

from .config import settings
from .handlers import router as core_router

logger = logging.getLogger(__name__)

bot = Bot(token=settings.bot_token, parse_mode="HTML")
dispatcher = Dispatcher()
dispatcher.include_router(core_router)


@asynccontextmanager
async def lifespan(_: FastAPI):
    polling_task: asyncio.Task | None = None
    configure_bot = not settings.is_placeholder_token()
    if configure_bot:
        try:
            if settings.webhook_url:
                await bot.set_webhook(
                    url=settings.webhook_url,
                    secret_token=settings.webhook_secret,
                    drop_pending_updates=True,
                )
            else:
                await bot.delete_webhook(drop_pending_updates=True)
                polling_task = asyncio.create_task(dispatcher.start_polling(bot))
        except TelegramUnauthorizedError:
            logger.warning("Telegram token unauthorized; skipping webhook/polling setup.")
            configure_bot = False
    try:
        yield
    finally:
        if polling_task:
            polling_task.cancel()
            with suppress(asyncio.CancelledError):
                await polling_task
        await bot.session.close()


app = FastAPI(title="EduQuest Bot", lifespan=lifespan)


@app.get("/health")
async def health() -> JSONResponse:
    return JSONResponse({"status": "ok"})


@app.post("/webhook")
async def telegram_webhook(request: Request) -> dict[str, bool]:
    if settings.webhook_secret:
        secret = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
        if secret != settings.webhook_secret:
            raise HTTPException(status_code=403, detail="Invalid webhook secret")

    update = Update.model_validate(await request.json())
    await dispatcher.feed_update(bot, update)
    return {"ok": True}


async def main() -> None:  # pragma: no cover
    if settings.is_placeholder_token():
        print("Placeholder bot token detected; polling is disabled.")
        return
    await dispatcher.start_polling(bot)


if __name__ == "__main__":  # pragma: no cover
    asyncio.run(main())
