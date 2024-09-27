import asyncio
import logging
import sys
import json

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import Message

TOKEN = "8041713572:AAESTo0FRRpIGIJsdxLEk-CRF965bx8Vl1A"

dp = Dispatcher()

states = dict()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    kb = [KeyboardButton(text='Записать сообщение'),
          KeyboardButton(text='Отправить сообщение')]
    kb_markup = ReplyKeyboardMarkup(keyboard=[kb], resize_keyboard=True)
    await message.answer(f"Привет, {html.bold(message.from_user.full_name)}!",
                         reply_markup=kb_markup)


@dp.message(F.text == 'Записать сообщение')
async def write_handler(message: Message) -> None:
    states[message.from_user.id] = 'wait_message'
    await message.answer("запишите сообщение")

@dp.message(F.text == 'Отправить сообщение')
async def send_handler(message: Message) -> None:
    with open("messages.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        try:
            result = data[str(message.from_user.id)]
            await message.answer(result)
        except KeyError:
            await message.answer("Сообщения отсутствуют")

@dp.message()
async def message_handler(message: Message) -> None:
    if states[message.from_user.id] == 'wait_message':
        with open("messages.json", "r+", encoding="utf-8") as file:
            data = json.load(file)
            data[str(message.from_user.id)] = message.text
            file.seek(0)
            json.dump(data, file)
            file.truncate()
        states[message.from_user.id] = None
        await message.answer("сообщение успешно записано")

async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
