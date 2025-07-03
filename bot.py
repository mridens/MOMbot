import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import CommandStart
from dotenv import load_dotenv
import os
import json

load_dotenv()

API_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

REQUIRED_CHANNELS = [
    "@mascaridens",
    "@testov121234",
    "@testov1212345"
]

async def check_subscriptions(user_id):
    for channel in REQUIRED_CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status in ['left', 'kicked']:
                return False
        except Exception:
            return False
    return True

@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    if await check_subscriptions(user_id):
        await message.answer("Спасибо за подписку! Вот ваш материал: https://example.com")
    else:
        channels_list = "\\n".join(REQUIRED_CHANNELS)
        await message.answer(f"Пожалуйста, подпишитесь на все каналы:\n{channels_list}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
