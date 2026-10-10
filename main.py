
import asyncio
import logging
import sys
import os
import random

from dotenv import load_dotenv
from zoneinfo import ZoneInfo

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from datetime import *

meeting_date = datetime(2026, 10, 24)

days_left = (meeting_date - datetime.now()).days


load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
KOSTIK_CHAT_ID = os.getenv("KOSTIK_CHAT_ID")
DASHUSHA_CHAT_ID = os.getenv("DASHUSHA_CHAT_ID")

if not TOKEN:
    raise RuntimeError("BOT_TOKEN не задан в .env")

if not KOSTIK_CHAT_ID:
    raise RuntimeError("KOSTIK_CHAT_ID не задан в .env")

if not DASHUSHA_CHAT_ID:
    raise RuntimeError("DASHUSHA_CHAT_ID не задан в .env")

KOSTIK_CHAT_ID = int(KOSTIK_CHAT_ID)
DASHUSHA_CHAT_ID = int(DASHUSHA_CHAT_ID)

dp = Dispatcher()
scheduler = AsyncIOScheduler(
    timezone=ZoneInfo("Europe/Moscow")
)

@dp.message(F.sticker)
async def get_sticker_id(message: Message):
    print(message.sticker.file_id)

'''Кнопачки'''


def get_reminder_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="я выпилаа муррр",
                    callback_data="medicine_taken"
                )
            ]
        ]
    )


def get_take_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="я взялаа мяяяяу",
                    callback_data="medicine_packed"
                )
            ]
        ]
    )


def get_love_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="и я тебя люблю коотиккк",
                    callback_data="love_answer"
                )
            ]
        ]
    )


'''напоминание о встрече'''


async def remind_meeting(bot: Bot):
    days_left = (meeting_date.date() - datetime.now().date()).days
    random_number = random.randint(0,6)

    phrases = [
        'скучаааю по тебе очень',
        'а я люблю тебя кисяяяя',
        'мурмяяяу',
        'а я хачу тя есле честна очень',
        'воотт а еще ти самая лучшая кися в мире бтв кстати',
        'го трахца паже',
        'таво рот ибал как я па тебе скучааааюююююю я б тя мяу'
    ]

    if days_left > 0:
        text = (
            f"кисяо до нашей встречи осталось {days_left} "
            f"{'день' if days_left == 1 else 'дня ' if days_left in (2, 3, 4) else 'дней '}"
            f"{phrases[random_number]}"
        )
    elif days_left == 0:
        text = "седня увидимся нах)"
    else:
        text = "люблю тебя моя кисенька"

    await bot.send_message(
        chat_id=KOSTIK_CHAT_ID,
        text=text
    )

    await bot.send_message(
        chat_id=DASHUSHA_CHAT_ID,
        text=text
    )

    await bot.send_sticker(
        chat_id=DASHUSHA_CHAT_ID,
        sticker="CAACAgIAAxkBAANbaspSYu_wY5sbop4WwbOI1HcXOioAAvkQAAIc-slLmjOQytI1kpI9BA"
    )

    await bot.send_sticker(
        chat_id=KOSTIK_CHAT_ID,
        sticker="CAACAgIAAxkBAANbaspSYu_wY5sbop4WwbOI1HcXOioAAvkQAAIc-slLmjOQytI1kpI9BA"
    )


'''повторение напоминаний'''

async def repeat_reminder(bot: Bot, kind: str):
    if kind == "medicine":
        await bot.send_message(
            chat_id=DASHUSHA_CHAT_ID,
            text="дашуша ты выпила уже или чо там нах",
            reply_markup=get_reminder_keyboard()
        )

    elif kind == "packed":
        await bot.send_message(
            chat_id=DASHUSHA_CHAT_ID,
            text="кисяо ты взяла анканкутанг нах?",
            reply_markup=get_take_keyboard()
        )


def start_repeating(bot: Bot, kind: str):
    scheduler.add_job(
        repeat_reminder,
        "interval",
        seconds=15,  # для теста; потом поменяешь на 15 * 60
        args=[bot, kind],
        id=f"repeat_{kind}",
        replace_existing=True
    )


def stop_repeating(kind: str):
    job_id = f"repeat_{kind}"
    job = scheduler.get_job(job_id)

    if job:
        scheduler.remove_job(job_id)


'''ежедневные напоминалки'''

async def remind_dasha(bot: Bot):
    await bot.send_message(
        chat_id=DASHUSHA_CHAT_ID,
        text="дашуша не забудь выпить анкакунанг",
        reply_markup=get_reminder_keyboard()
    )

    start_repeating(bot, "medicine")


async def remind_to_take(bot: Bot):
    await bot.send_message(
        chat_id=DASHUSHA_CHAT_ID,
        text="не забудь взять анкакутанг с сабой, люблю тя",
        reply_markup=get_take_keyboard()
    )

    start_repeating(bot, "packed")


'''обработчики'''

@dp.message(CommandStart())
async def command_start_handler(message: Message):
    await message.answer("мяу")


@dp.message(F.text.lower() == "люблю тебя")
async def love_handler(message: Message):
    await message.answer("и я тебя люблю кисенька мояяя")


@dp.callback_query(F.data == "medicine_taken")
async def medicine_taken_handler(callback: CallbackQuery, bot: Bot):
    if callback.from_user.id != KOSTIK_CHAT_ID:
        await callback.answer("эта кнопочка не для тебя мурр")
        return

    stop_repeating("medicine")
    await callback.answer("умничкааа")

    await callback.message.answer(
        "ой вай ахуена умничка"
    )

    await callback.message.answer(
        text="люблю тя нах",
        reply_markup=get_love_keyboard()
    )

    await bot.send_message(
        chat_id=KOSTIK_CHAT_ID,
        text="киса отметила что выпила акннактгг"
    )


@dp.callback_query(F.data == "medicine_packed")
async def medicine_packed_handler(callback: CallbackQuery, bot: Bot):
    if callback.from_user.id != KOSTIK_CHAT_ID:
        await callback.answer("эта кнопочка не для тебя мяу")
        return

    stop_repeating("packed")
    await callback.answer("умничка кисенька")

    await callback.message.answer(
        "умничкааа кисааааа четкава дня те там нах а я сплю еще бтв кстати вот"
    )

    await bot.send_message(
        chat_id=KOSTIK_CHAT_ID,
        text="киса отметила что взяла аканкуаин с собой"
    )


@dp.callback_query(F.data == "love_answer")
async def love_answer_handler(callback: CallbackQuery, bot: Bot):
    await callback.answer("и я тебя люблюю")

    await bot.send_sticker(
        chat_id=callback.message.chat.id,
        sticker="CAACAgIAAxkBAAMiaspDk1Q2UUY70nvF_6jcDEjbdQQAAkAZAAKW9gABSEuv9AZMUOTRPQQ"
    )

    await bot.send_message(
        chat_id=KOSTIK_CHAT_ID,
        text="киса нажала кнопку что любит"
    )



'''запуск'''

async def main() -> None:
    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )

    scheduler.add_job(
        remind_dasha,
        "cron",
        hour=12,
        minute=0,
        args=[bot],
        id="daily_medicine",
        replace_existing=True
    )

    scheduler.add_job(
        remind_to_take,
        "cron",
        hour=6,
        minute=0,
        args=[bot],
        id="daily_packed",
        replace_existing=True
    )

    scheduler.add_job(
        remind_meeting,
        "cron",
        hour=19,
        minute=10,
        args=[bot],
        id="daily_meeting",
        replace_existing=True
    )

    scheduler.start()

    # await remind_dasha(bot)
    # await remind_to_take(bot)

    try:
        await dp.start_polling(bot)
    finally:
        scheduler.shutdown(wait=False)
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout
    )
    asyncio.run(main())
