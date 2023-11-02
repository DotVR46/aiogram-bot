# Тут будет Телеграм Бот
import os
import asyncio
from aiogram import Bot, Dispatcher, types

from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")


async def main():
    pass


if __name__ == "__main__":
    asyncio.run(main())
