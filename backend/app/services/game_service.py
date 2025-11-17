from __future__ import annotations

from collections.abc import Iterable
from datetime import date, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import settings
from ..data import TASKS_PLAN, resolve_goal_template
from ..models import DailyGoal, DailyGoalStatus, Task, TaskStatus, User, UserTask
from ..schemas import AttributeSchema, DailyGoalSchema, HealthSchema, ProgressSchema, TaskPreview, UserStateResponse


async def ensure_user(session: AsyncSession, telegram_id: int, username: str | None) -> User:
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalar_one_or_none()

    if user:
        if username and user.username != username:
            user.username = username
            await session.flush()
        return user

    user = User(telegram_id=telegram_id, username=username)
    session.add(user)
    await session.flush()
    await assign_initial_tasks(session, user)
    await ensure_daily_goals(session, user)
    await session.commit()
    return user


def _program_day_number(user: User, target_date: date) -> int:
    base = (user.created_at or datetime.utcnow()).date()
    return (target_date - base).days


async def ensure_task_catalog(session: AsyncSession) -> dict[str, Task]:
    result = await session.execute(select(Task))
    tasks = result.scalars().all()
    tasks_by_title = {task.title: task for task in tasks}
    created = False

    for task_template in TASKS_PLAN:
        if task_template["title"] in tasks_by_title:
            continue
        task = Task(
            title=task_template["title"],
            description=task_template["description"],
            difficulty=task_template["difficulty"],
            xp_reward=task_template["xp_reward"],
            health_delta=task_template["health_delta"],
        )
        session.add(task)
        tasks_by_title[task.title] = task
        created = True

    if created:
        await session.flush()

    return tasks_by_title


async def assign_initial_tasks(session: AsyncSession, user: User) -> None:
    existing_assignments = await session.execute(select(UserTask.id).where(UserTask.user_id == user.id))
    if existing_assignments.first():
        return

    tasks_by_title = await ensure_task_catalog(session)
    base_date = (user.created_at or datetime.utcnow()).date()

    assignments = []
    for index, template in enumerate(TASKS_PLAN):
        task = tasks_by_title[template["title"]]
        assignments.append(
            UserTask(
                user_id=user.id,
                task_id=task.id,
                status=TaskStatus.pending,
                order_index=index,
                available_on=base_date + timedelta(days=int(template.get("day_offset", 0))),
            )
        )

    session.add_all(assignments)
    await session.flush()


async def ensure_daily_goals(
    session: AsyncSession,
    user: User,
    target_dates: Iterable[date] | None = None,
) -> None:
    if target_dates is None:
        target_dates = [date.today() + timedelta(days=delta) for delta in (-1, 0, 1)]

    created = False
    for target_date in target_dates:
        existing = await session.execute(
            select(DailyGoal).where(DailyGoal.user_id == user.id, DailyGoal.date == target_date)
        )
        goal = existing.scalar_one_or_none()
        if goal:
            continue

        day_number = _program_day_number(user, target_date)
        template = resolve_goal_template(day_number)
        session.add(
            DailyGoal(
                user_id=user.id,
                date=target_date,
                title=template.title,
                description=template.description,
                status=DailyGoalStatus.pending,
            )
        )
        created = True

    if created:
        await session.flush()


async def get_user_state(session: AsyncSession, user: User) -> UserStateResponse:
    await ensure_daily_goals(session, user)

    result = await session.execute(
        select(UserTask)
        .where(
            UserTask.user_id == user.id,
            UserTask.status != TaskStatus.completed,
            UserTask.available_on <= date.today(),
        )
        .order_by(UserTask.available_on, UserTask.order_index)
    )
    tasks = result.scalars().all()
    current_assignment = tasks[0] if tasks else None
    current_task = None

    if current_assignment:
        await session.refresh(current_assignment, attribute_names=["task"])
        current_task = TaskPreview(
            id=current_assignment.task.id,
            title=current_assignment.task.title,
            description=current_assignment.task.description,
            difficulty=current_assignment.task.difficulty,
            status=current_assignment.status,
            xp_reward=current_assignment.task.xp_reward,
            health_delta=current_assignment.task.health_delta,
        )

    goals = await session.execute(select(DailyGoal).where(DailyGoal.user_id == user.id))
    goals_by_date = {goal.date: goal for goal in goals.scalars().all()}

    def serialize_goal(target_date: date) -> DailyGoalSchema | None:
        goal = goals_by_date.get(target_date)
        if not goal:
            return None
        return DailyGoalSchema(
            id=goal.id,
            date=goal.date,
            title=goal.title,
            description=goal.description,
            status=goal.status,
        )

    attributes = [
        AttributeSchema(name=key, value=value)
        for key, value in sorted((user.attributes or {}).items(), key=lambda item: item[0])
    ]

    xp_per_level = max(settings.xp_per_level, 1)
    experience_in_level = user.experience % xp_per_level
    experience_to_next_level = xp_per_level - experience_in_level if experience_in_level != 0 else xp_per_level
    level_completion_percent = (experience_in_level / xp_per_level) * 100

    return UserStateResponse(
        user_id=user.id,
        username=user.username,
        health=HealthSchema(current=user.health_points, max=settings.health_points_default),
        progress=ProgressSchema(
            level=user.level,
            experience=user.experience,
            experience_in_level=experience_in_level,
            experience_to_next_level=experience_to_next_level,
            level_completion_percent=level_completion_percent,
        ),
        attributes=attributes,
        current_task=current_task,
        backlog_size=len(tasks[1:]),
        goals={
            "yesterday": serialize_goal(date.today() - timedelta(days=1)),
            "today": serialize_goal(date.today()),
            "tomorrow": serialize_goal(date.today() + timedelta(days=1)),
        },
    )


async def complete_task(
    session: AsyncSession,
    *,
    user: User,
    task_id: int,
    completed_at: datetime | None = None,
) -> UserStateResponse:
    result = await session.execute(
        select(UserTask)
        .where(UserTask.user_id == user.id, UserTask.task_id == task_id)
        .limit(1)
    )
    assignment = result.scalar_one_or_none()
    if not assignment:
        raise ValueError("Task not assigned to user")

    if assignment.available_on > date.today():
        raise ValueError("Task недоступна для выполнения сегодня")

    await session.refresh(assignment, attribute_names=["task"])

    assignment.status = TaskStatus.completed
    assignment.completed_at = completed_at or datetime.utcnow()

    user.experience += assignment.task.xp_reward
    user.health_points = max(0, min(settings.health_points_default, user.health_points + assignment.task.health_delta))

    await session.flush()

    return await get_user_state(session, user)
