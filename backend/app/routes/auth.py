from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db_session
from ..schemas import InitPayload, InitRequest, UserStateResponse
from ..services.game_service import ensure_user, get_user_state
from ..utils.telegram import parse_init_data

router = APIRouter(prefix="/auth")


@router.post("/init", response_model=UserStateResponse)
async def handle_init(payload: InitRequest, session: AsyncSession = Depends(get_db_session)) -> UserStateResponse:
    telegram_payload: InitPayload = parse_init_data(payload.init_data)
    user = await ensure_user(session, telegram_payload.user.id, telegram_payload.user.username)
    return await get_user_state(session, user)
