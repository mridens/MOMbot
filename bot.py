from aiogram import Bot, Dispatcher, executor, types
import logging
import asyncio
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv('BOT_TOKEN')
REQUIRED_CHANNELS = ['@mascaridens', '@testov121234', '@testov1212345']

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

USERS_FILE = 'users.json'

def load_users():
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

async def check_subscription(user_id, channel):
    try:
        member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
        return member.is_chat_member()
    except:
        return False

async def check_all_subscriptions(user_id):
    for ch in REQUIRED_CHANNELS:
        if not await check_subscription(user_id, ch):
            return False
    return True

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    if await check_all_subscriptions(user_id):
        await message.answer("Подписка есть ✅")
        users = load_users()
        if user_id not in users:
            users.append(user_id)
            save_users(users)
    else:
        await message.answer("Проверьте подписку ещё раз ❌\nПодпишитесь на все каналы и нажмите /check")

@dp.message_handler(commands=['check'])
async def check_handler(message: types.Message):
    user_id = message.from_user.id
    if await check_all_subscriptions(user_id):
        await message.answer("Подписка есть ✅")
        users = load_users()
        if user_id not in users:
            users.append(user_id)
            save_users(users)
    else:
        await message.answer("Проверьте подписку ещё раз ❌")

@dp.message_handler(commands=['broadcast'])
async def broadcast_handler(message: types.Message):
    admin_id = 123456789  # <- вставь сюда свой Telegram ID
    if message.from_user.id != admin_id:
        return
    users = load_users()
    if not users:
        await message.answer("Нет подписчиков для рассылки.")
        return
    text = "Вот ваша ссылка на материалы: https://example.com/material.pdf"
    count = 0
    for user_id in users:
        try:
            await bot.send_message(user_id, text)
            count += 1
            await asyncio.sleep(0.1)
        except Exception as e:
            print(f"Не удалось отправить пользователю {user_id}: {e}")
    await message.answer(f"Рассылка выполнена, отправлено сообщений: {count}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
