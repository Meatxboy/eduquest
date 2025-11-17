from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from ..models import TaskDifficulty


@dataclass(frozen=True)
class TaskBlock:
    title: str
    difficulty: TaskDifficulty
    xp_reward: int
    health_delta: int
    day_offset: int
    steps: tuple[str, ...]


@dataclass(frozen=True)
class GoalTemplate:
    day_offset: int
    title: str
    description: str


RAW_TASK_BLOCKS: tuple[TaskBlock, ...] = (
    TaskBlock(
        title="Ежедневная микро-рефлексия — Задача 1. Выбрать фиксированное время",
        difficulty=TaskDifficulty.easy,
        xp_reward=12,
        health_delta=0,
        day_offset=0,
        steps=(
            "Проверить своё расписание на неделю",
            "Определить самое спокойное время",
            "Поставить напоминание в календарь",
        ),
    ),
    TaskBlock(
        title="Ежедневная микро-рефлексия — Задача 2. Создать шаблон заметки",
        difficulty=TaskDifficulty.easy,
        xp_reward=15,
        health_delta=0,
        day_offset=0,
        steps=(
            "Открыть заметки, Notion или Google Docs",
            "Создать файл «Рефлексия — неделя»",
            "Добавить три вопроса",
            "Что дало энергию?",
            "Что забрало энергию?",
            "Какое решение было осознанным/импульсивным?",
            "Разметить 7 блоков по дням",
        ),
    ),
    TaskBlock(
        title="Ежедневная микро-рефлексия — Задача 3. Заполнять ежедневно",
        difficulty=TaskDifficulty.medium,
        xp_reward=18,
        health_delta=0,
        day_offset=0,
        steps=(
            "Открывать заметку в выбранное время",
            "Кратко отвечать на три вопроса",
            "Отмечать эмоциональный фон (1–5)",
        ),
    ),
    TaskBlock(
        title="Ежедневная микро-рефлексия — Задача 4. Итоговый обзор",
        difficulty=TaskDifficulty.medium,
        xp_reward=20,
        health_delta=5,
        day_offset=0,
        steps=(
            "Прочитать записи за неделю",
            "Найти повторяющиеся темы",
            "Записать итоговый вывод",
        ),
    ),
    TaskBlock(
        title="Наблюдение за автоматическими реакциями — Задача 1. Настроить напоминания",
        difficulty=TaskDifficulty.easy,
        xp_reward=12,
        health_delta=0,
        day_offset=1,
        steps=(
            "Поставить два напоминания (например, 12:00 и 17:00)",
            "Добавить текст «Проверь реакцию — тело/эмоции»",
        ),
    ),
    TaskBlock(
        title="Наблюдение за автоматическими реакциями — Задача 2. Отслеживать реакции в моменте",
        difficulty=TaskDifficulty.medium,
        xp_reward=18,
        health_delta=0,
        day_offset=1,
        steps=(
            "Остановиться на 5–10 секунд",
            "Замечать реакцию: напряжение, раздражение, спешка",
            "Определять контекст: где, кто и почему",
        ),
    ),
    TaskBlock(
        title="Наблюдение за автоматическими реакциями — Задача 3. Записывать короткие заметки",
        difficulty=TaskDifficulty.medium,
        xp_reward=18,
        health_delta=0,
        day_offset=1,
        steps=(
            "Создать файл «Автоматические реакции»",
            "Формат записи: ситуация → реакция → причина",
            "Делать 1–3 записи в день",
        ),
    ),
    TaskBlock(
        title="Наблюдение за автоматическими реакциями — Задача 4. Найти триггеры",
        difficulty=TaskDifficulty.medium,
        xp_reward=20,
        health_delta=5,
        day_offset=1,
        steps=(
            "Просмотреть все заметки",
            "Отметить повторяющиеся ситуации",
            "Выделить 2 главных триггера недели",
        ),
    ),
    TaskBlock(
        title="Один час без внешних стимулов — Задача 1. Выбрать время",
        difficulty=TaskDifficulty.easy,
        xp_reward=12,
        health_delta=5,
        day_offset=2,
        steps=(
            "Определить свободный день",
            "Заблокировать 1 час",
            "Занести его в календарь",
        ),
    ),
    TaskBlock(
        title="Один час без внешних стимулов — Задача 2. Выбрать формат",
        difficulty=TaskDifficulty.medium,
        xp_reward=16,
        health_delta=5,
        day_offset=2,
        steps=(
            "Рассмотреть формат прогулки",
            "Рассмотреть формат горячей ванны",
            "Рассмотреть формат чая или тишины",
            "Подготовить всё заранее",
        ),
    ),
    TaskBlock(
        title="Один час без внешних стимулов — Задача 3. Убрать стимулы",
        difficulty=TaskDifficulty.medium,
        xp_reward=18,
        health_delta=8,
        day_offset=2,
        steps=(
            "Отключить уведомления",
            "Положить телефон в другое место",
            "Исключить музыку и разговоры",
        ),
    ),
    TaskBlock(
        title="Один час без внешних стимулов — Задача 4. Подвести итог",
        difficulty=TaskDifficulty.medium,
        xp_reward=20,
        health_delta=10,
        day_offset=2,
        steps=(
            "После часа посидеть 1 минуту спокойно",
            "Записать 3 мысли или ощущения",
            "Сохранить их в заметку",
        ),
    ),
    TaskBlock(
        title="Проверка истинных мотивов — Задача 1. Выбрать 3–5 решений недели",
        difficulty=TaskDifficulty.easy,
        xp_reward=14,
        health_delta=0,
        day_offset=3,
        steps=(
            "Просмотреть задачи недели",
            "Выбрать важные решения",
            "Создать список",
        ),
    ),
    TaskBlock(
        title="Проверка истинных мотивов — Задача 2. Применять вопросы о мотивах",
        difficulty=TaskDifficulty.medium,
        xp_reward=18,
        health_delta=0,
        day_offset=3,
        steps=(
            "Делать паузу перед согласием",
            "Задавать вопросы «Я хочу или надо?»",
            "Задавать вопросы «Чей это мотив?»",
        ),
    ),
    TaskBlock(
        title="Проверка истинных мотивов — Задача 3. Фиксировать мотивы",
        difficulty=TaskDifficulty.medium,
        xp_reward=18,
        health_delta=0,
        day_offset=3,
        steps=(
            "Создать заметку «Мотивы решений»",
            "Использовать формат решение → мотив → ощущение",
            "Заполнять заметку в течение недели",
        ),
    ),
    TaskBlock(
        title="Проверка истинных мотивов — Задача 4. Анализ",
        difficulty=TaskDifficulty.medium,
        xp_reward=20,
        health_delta=5,
        day_offset=3,
        steps=(
            "Пройтись по списку",
            "Отметить решения, где мотив был внешним",
            "Сформулировать, что изменить на следующей неделе",
        ),
    ),
    TaskBlock(
        title="Ведение дневника смыслов — Задача 1. Создать дневник",
        difficulty=TaskDifficulty.easy,
        xp_reward=12,
        health_delta=0,
        day_offset=4,
        steps=(
            "Открыть документ",
            "Назвать его «Дневник смыслов — неделя»",
            "Сделать 3 блока: Пн–Вт / Ср–Чт / Пт–Вс",
        ),
    ),
    TaskBlock(
        title="Ведение дневника смыслов — Задача 2. Писать 2–3 раза в неделю",
        difficulty=TaskDifficulty.medium,
        xp_reward=18,
        health_delta=0,
        day_offset=4,
        steps=(
            "Найти 10 минут",
            "Ответить на два вопроса",
            "Что важно для меня сейчас?",
            "Что хочу сохранить после недели?",
        ),
    ),
    TaskBlock(
        title="Ведение дневника смыслов — Задача 3. Отмечать повторения",
        difficulty=TaskDifficulty.medium,
        xp_reward=16,
        health_delta=0,
        day_offset=4,
        steps=(
            "Перечитывать записи",
            "Помечать повторяющиеся темы",
        ),
    ),
    TaskBlock(
        title="Ведение дневника смыслов — Задача 4. Главная ценность недели",
        difficulty=TaskDifficulty.medium,
        xp_reward=20,
        health_delta=5,
        day_offset=4,
        steps=(
            "Просмотреть все записи",
            "Найти повторяющуюся ценность",
            "Записать её отдельно",
        ),
    ),
    TaskBlock(
        title="Телесная осознанность — Задача 1. Выбрать время",
        difficulty=TaskDifficulty.easy,
        xp_reward=12,
        health_delta=5,
        day_offset=5,
        steps=(
            "Определить утро или вечер",
            "Поставить напоминание",
        ),
    ),
    TaskBlock(
        title="Телесная осознанность — Задача 2. Сканирование тела",
        difficulty=TaskDifficulty.medium,
        xp_reward=18,
        health_delta=8,
        day_offset=5,
        steps=(
            "Сесть удобно",
            "Пройти вниманием сверху вниз",
            "Отмечать зажимы и мягко отпускать",
        ),
    ),
    TaskBlock(
        title="Телесная осознанность — Задача 3. Дыхание 4–7–8",
        difficulty=TaskDifficulty.medium,
        xp_reward=18,
        health_delta=10,
        day_offset=5,
        steps=(
            "Сесть ровно",
            "Сделать вдох на 4 секунды",
            "Задержать дыхание на 7 секунд",
            "Сделать выдох на 8 секунд",
            "Повторить цикл 3–4 раза",
        ),
    ),
    TaskBlock(
        title="Телесная осознанность — Задача 4. Отслеживание состояний",
        difficulty=TaskDifficulty.medium,
        xp_reward=18,
        health_delta=5,
        day_offset=5,
        steps=(
            "Спросить себя «Как сейчас тело?»",
            "Кратко записать наблюдение",
        ),
    ),
    TaskBlock(
        title="Итог недели — самоинтервью — Задача 1. Выделить время",
        difficulty=TaskDifficulty.easy,
        xp_reward=12,
        health_delta=0,
        day_offset=6,
        steps=(
            "Найти удобный день (пятница или суббота)",
            "Поставить напоминание",
        ),
    ),
    TaskBlock(
        title="Итог недели — самоинтервью — Задача 2. Ответить на вопросы",
        difficulty=TaskDifficulty.medium,
        xp_reward=20,
        health_delta=0,
        day_offset=6,
        steps=(
            "Что понял о себе?",
            "Что стал лучше замечать?",
            "Где ещё действую на автопилоте?",
            "Что беру в следующую неделю?",
        ),
    ),
    TaskBlock(
        title="Итог недели — самоинтервью — Задача 3. Зафиксировать выводы",
        difficulty=TaskDifficulty.medium,
        xp_reward=18,
        health_delta=5,
        day_offset=6,
        steps=(
            "Выделить 1–2 инсайта",
            "Записать их в финальный блок",
        ),
    ),
    TaskBlock(
        title="Итог недели — самоинтервью — Задача 4. Сформировать цели на следующую неделю",
        difficulty=TaskDifficulty.medium,
        xp_reward=20,
        health_delta=5,
        day_offset=6,
        steps=(
            "Определить направление развития",
            "Сформировать новый список целей",
            "Создать новый документ",
        ),
    ),
)


GOAL_TEMPLATES: tuple[GoalTemplate, ...] = (
    GoalTemplate(
        day_offset=0,
        title="Ежедневная микро-рефлексия",
        description="5–10 минут на ежедневную запись и отслеживание эмоционального фона.",
    ),
    GoalTemplate(
        day_offset=1,
        title="Наблюдение за автоматическими реакциями",
        description="Учимся замечать телесные и эмоциональные триггеры в течение дня.",
    ),
    GoalTemplate(
        day_offset=2,
        title="Один час без внешних стимулов",
        description="Выделяем защищённое окно тишины и отдыха без уведомлений.",
    ),
    GoalTemplate(
        day_offset=3,
        title="Проверка истинных мотивов",
        description="Разбираем ключевые решения недели и ищем истинные мотивы.",
    ),
    GoalTemplate(
        day_offset=4,
        title="Ведение дневника смыслов",
        description="Фиксируем ценности, повторяющиеся темы и важные выводы.",
    ),
    GoalTemplate(
        day_offset=5,
        title="Телесная осознанность",
        description="Практикуем сканирование тела и дыхание 4–7–8.",
    ),
    GoalTemplate(
        day_offset=6,
        title="Итог недели — самоинтервью",
        description="Подводим итоги, фиксируем инсайты и формируем новую неделю.",
    ),
)

ORDERED_GOAL_TEMPLATES = tuple(sorted(GOAL_TEMPLATES, key=lambda template: template.day_offset))
PROGRAM_LENGTH = len(ORDERED_GOAL_TEMPLATES)


def _distribute_value(total: int, count: int) -> list[int]:
    if count <= 0:
        return []
    base, remainder = divmod(total, count)
    values = [base] * count
    for index in range(remainder):
        values[index] += 1
    return values


def _flatten_blocks(blocks: Iterable[TaskBlock]) -> list[dict[str, object]]:
    flattened: list[dict[str, object]] = []
    for block in blocks:
        steps = list(block.steps)
        if not steps:
            continue

        xp_shares = _distribute_value(block.xp_reward, len(steps))
        health_shares = _distribute_value(block.health_delta, len(steps))

        for idx, step in enumerate(steps, start=1):
            flattened.append(
                {
                    "title": f"{block.title} — шаг {idx}. {step}",
                    "description": step,
                    "difficulty": block.difficulty,
                    "xp_reward": xp_shares[idx - 1] if xp_shares else 0,
                    "health_delta": health_shares[idx - 1] if health_shares else 0,
                    "day_offset": block.day_offset,
                }
            )
    return flattened


def resolve_goal_template(day_number: int) -> GoalTemplate:
    if not ORDERED_GOAL_TEMPLATES:
        raise ValueError("Goal templates are not configured")

    if day_number < 0:
        index = 0
    else:
        index = day_number % PROGRAM_LENGTH
    return ORDERED_GOAL_TEMPLATES[index]


TASKS_PLAN = _flatten_blocks(RAW_TASK_BLOCKS)


__all__ = ["TASKS_PLAN", "GOAL_TEMPLATES", "resolve_goal_template", "PROGRAM_LENGTH"]
