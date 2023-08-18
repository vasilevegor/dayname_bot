import asyncio
import logging
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.utils.markdown import hbold
from sqlalchemy import URL

from handlers import router, scheduler
from db import create_async_engine, get_session_maker

load_dotenv()

TOKEN = os.getenv("token")
        

async def on_startup(dp): 
    asyncio.create_task(scheduler())        


async def main() -> None:
    
    dp = Dispatcher()   
    dp.include_router(router)

    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot, on_startup=on_startup)
    
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


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped!")