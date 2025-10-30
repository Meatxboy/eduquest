from fastapi import APIRouter

from . import auth, state

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(state.router, tags=["state"])
