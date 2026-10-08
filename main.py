import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

import os
from dotenv import load_dotenv

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from zoneinfo import ZoneInfo


load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
DASHA_CHAT_ID = os.getenv("DASHA_CHAT_ID")
KOSTIK_CHAT_ID = os.getenv("KOSTIK_CHAT_ID")

if not TOKEN:
    raise RuntimeError("BOT_TOKEN не задан в .env")

if not DASHA_CHAT_ID:
    raise RuntimeError("DASHA_CHAT_ID не задан в .env")

if not KOSTIK_CHAT_ID:
    raise RuntimeError("KOSTIK_CHAT_ID не задан в .env")

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    print(f"chat_id: {message.chat.id}")
    await message.answer(f'67676767sixseven6767676767667676767sixseven6767676767667676767sixseven6767676767667676767sixseven6767676767667676767sixseven6767676767667676767sixseven6767676767667676767sixseven6767676767667676767sixseven6767676767667676767sixseven6767676767667676767sixseven6767676767667676767sixseven6767676767667676767sixseven6767676767667676767sixseven67676767676')


@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("kdvjnkjvnvjf")


async def remind_dasha(bot: Bot):
    await bot.send_message(
        chat_id=DASHA_CHAT_ID,
        text="дашуша не забудь выпить анкакунанг"
    )
    await bot.send_message(
        chat_id=KOSTIK_CHAT_ID,
        text="дашуша не забудь выпить анкакунанг"
    )
    await bot.send_message(
        chat_id=DASHA_CHAT_ID,
        text="люблю тя"
    )
    await bot.send_message(
        chat_id=KOSTIK_CHAT_ID,
        text="люблю тя"
    )

async def remind_to_take(bot: Bot):
    await bot.send_message(
        chat_id=DASHA_CHAT_ID,
        text="не забудь взять анкакутанг с сабой, люблю тя"
    )
    await bot.send_message(
        chat_id=KOSTIK_CHAT_ID,
        text="не забудь взять анкакутанг с сабой, люблю тя"
    )


async def main() -> None:
    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    scheduler = AsyncIOScheduler(
        timezone=ZoneInfo("Europe/Moscow")
    )

    scheduler.add_job(
        remind_dasha,
        "cron",
        hour=12,
        minute=00,
        args=[bot]
    )

    scheduler.add_job(
        remind_to_take,
        "cron",
        hour=6,
        minute=00,
        args=[bot]
    )

    scheduler.start()

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
