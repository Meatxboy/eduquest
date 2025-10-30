from __future__ import annotations

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from .cache import get_redis
from .config import settings
from .database import engine, get_db_session
from .models import Base
from .observability import register_metrics, setup_logging
from .routes import api_router

setup_logging()
app = FastAPI(title=settings.app_name, version="0.1.0", docs_url="/docs")
register_metrics(app)


@app.on_event("startup")
async def on_startup() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def on_shutdown() -> None:
    await engine.dispose()
    redis = get_redis()
    await redis.close()


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["health"])
async def healthcheck(session: AsyncSession = Depends(get_db_session)) -> JSONResponse:
    await session.execute(text("SELECT 1"))
    return JSONResponse({"status": "ok"})


app.include_router(api_router)


# Convenience entry point for local runs
async def lifespan() -> None:  # pragma: no cover
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":  # pragma: no cover
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
