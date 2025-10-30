from __future__ import annotations

from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, Field

from .models import DailyGoalStatus, TaskDifficulty, TaskStatus


class TelegramUserPayload(BaseModel):
    id: int
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None


class InitPayload(BaseModel):
    user: TelegramUserPayload
    auth_date: int
    hash: str


class InitRequest(BaseModel):
    init_data: str


class AttributeSchema(BaseModel):
    name: str
    value: int


class TaskPreview(BaseModel):
    id: int
    title: str
    description: str | None
    difficulty: TaskDifficulty
    status: TaskStatus
    xp_reward: int
    health_delta: int


class DailyGoalSchema(BaseModel):
    id: int
    date: date
    title: str
    description: str | None
    status: DailyGoalStatus


class ProgressSchema(BaseModel):
    level: int
    experience: int
    experience_in_level: int
    experience_to_next_level: int
    level_completion_percent: float


class HealthSchema(BaseModel):
    current: int
    max: int


class UserStateResponse(BaseModel):
    user_id: int
    username: str | None
    health: HealthSchema
    progress: ProgressSchema
    attributes: list[AttributeSchema]
    current_task: TaskPreview | None
    backlog_size: int = Field(ge=0)
    goals: dict[str, DailyGoalSchema | None]


class CompleteTaskRequest(BaseModel):
    task_id: int
    completed_at: datetime | None = None


class CompleteTaskResponse(BaseModel):
    success: bool
    new_state: UserStateResponse


class ErrorResponse(BaseModel):
    detail: str
    extra: dict[str, Any] | None = None
