import asyncio
import logging
import sys

from aiogram import Dispatcher
from bot.bot import bot

from bot.user.handlers import router as user_router
from bot.admin.handlers import router as admin_router

from bot.middleware import MediaGroupMiddleware

import db.db as db


async def main():
    await db.create_tables()
    dp = Dispatcher()
    dp.message.middleware(MediaGroupMiddleware())

    dp.include_router(admin_router)
    dp.include_router(user_router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    logging.getLogger('sqlalchemy.engine.Engine').disabled = True
    try:
        asyncio.run(main())
    except Exception as e:
        print(e)
