import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from sqlalchemy import URL
from dotenv import load_dotenv


from db import create_async_engine, get_session_maker
from handlers import router


load_dotenv()

TOKEN = os.getenv("token")


async def main() -> None:
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.include_router(router)

    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

    postgres_url = URL.create(
        "postgresql+asyncpg",
        username=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=int(os.getenv("POSTGRES_PORT")),
        database=os.getenv("POSTGRES_DB"),
    )

    async_engine = create_async_engine(postgres_url)
    session_maker = get_session_maker(async_engine)

    await dp.start_polling(bot, session_maker=session_maker)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    try:
        asyncio.run(main())
        # scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped!")
