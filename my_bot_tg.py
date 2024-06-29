import logging.handlers
from aiogram import Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import AsyncSession

from art import tprint
from colorama import Fore, init
import asyncio
import logging
from database.engine import create_db, session_maker
from middlewares.db import DataBaseSession

from handlers import client, my, weathers, expenses, books, magic_ball
from config import bot, storage
from dotenv import load_dotenv
import os

load_dotenv()



async def on_startup():
    try:
        await create_db()
        text = 'Database is running!\nBot is running!'
        print(Fore.GREEN + text)
    except Exception as ex:
        text = str(ex)
        print(Fore.RED + text)
    await bot.send_message(chat_id=int(os.getenv('ADMIN')), text=text)


async def main():
    format = ('%(asctime)s - [%(levelname)s] - %(name)s - [%(module)s]'
              "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")
    logging.basicConfig(level=logging.INFO, format=format, filename='bot.txt')

    dp = Dispatcher(storage=storage)
    dp.include_routers(
        books.books_router, client.client_router, weathers.weather_router, expenses.expenses_router,
        magic_ball.magic_ball_routers, my.my_router)
    dp.startup.register(on_startup)
    dp.update.middleware(DataBaseSession(session_pool=session_maker))

    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(weathers.down_weather, 'cron', hour="*/12")
    scheduler.add_job(weathers.auto_weather, 'cron', hour=5, minute=1,)
    scheduler.add_job(my.birthday, 'cron', day_of_week='mon-sun',
                      hour=5, args=(my.my_router, AsyncSession))
    scheduler.start()

    init(autoreset=True)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()

if __name__ == "__main__":
    tprint('Start Bot', font='doom', space=2)
    asyncio.run(main())
