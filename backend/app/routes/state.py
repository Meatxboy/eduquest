from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db_session
from ..models import User
from ..schemas import CompleteTaskRequest, CompleteTaskResponse, ErrorResponse, UserStateResponse
from ..services.game_service import complete_task, ensure_user, get_user_state

router = APIRouter(prefix="/state")


async def resolve_user(
    telegram_id: int = Query(..., description="Telegram user identifier"),
    username: str | None = Query(None, description="Telegram username"),
    session: AsyncSession = Depends(get_db_session),
) -> tuple[User, AsyncSession]:
    user = await ensure_user(session, telegram_id=telegram_id, username=username)
    return user, session


@router.get("", response_model=UserStateResponse)
async def read_state(user_and_session: tuple[User, AsyncSession] = Depends(resolve_user)) -> UserStateResponse:
    user, session = user_and_session
    return await get_user_state(session, user)


@router.post("/tasks/complete", response_model=CompleteTaskResponse, responses={404: {"model": ErrorResponse}})
async def mark_task_completed(
    payload: CompleteTaskRequest,
    user_and_session: tuple[User, AsyncSession] = Depends(resolve_user),
) -> CompleteTaskResponse:
    user, session = user_and_session
    try:
        new_state = await complete_task(
            session,
            user=user,
            task_id=payload.task_id,
            completed_at=payload.completed_at,
        )
    except ValueError as exc:  # pragma: no cover - defensive branch
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    await session.commit()
    return CompleteTaskResponse(success=True, new_state=new_state)
