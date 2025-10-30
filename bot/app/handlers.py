from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, WebAppInfo

from .config import settings


router = Router()


@router.message(CommandStart())
async def handle_start(message: Message) -> None:
    await message.answer(
        "Привет! Запусти мини-приложение, чтобы увидеть свою задачу дня.",
        reply_markup=ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [
                    KeyboardButton(
                        text="Открыть мини-приложение",
                        web_app=WebAppInfo(url=settings.frontend_base_url),
                    )
                ]
            ],
        ),
    )


@router.message(Command("help"))
async def handle_help(message: Message) -> None:
    await message.answer(
        "Я помогу тебе отслеживать прогресс и задачи. Нажми кнопку мини-приложения, чтобы начать!"
    )
