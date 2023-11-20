import os
import asyncio
import logging

from aiogram.enums import ParseMode
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from database.connection import session, Post

load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL = "@baphometme"
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# Функция для отправки новости
async def send_news():
    async with session:
        # Получаем неопубликованные новости
        news = await session.execute(
            Post.__table__.select().where(Post.posted == False).limit(1)
        )
        news_item = news.fetchone()

        if news_item:
            # Отправляем новость в канал
            await bot.send_photo(
                chat_id=CHANNEL,
                photo=news_item.image_url,
                caption=f"""<b>{news_item.post_title}</b>\n \n {news_item.post_url}""",
                # caption=news_item.post_url,
                parse_mode=ParseMode.HTML,
            )

            # await bot.send_message(
            #     chat_id=CHANNEL,
            #     text=news_item.post_url,
            #     parse_mode=ParseMode.HTML,
            # )

            # Обновляем флаг "опубликовано" в базе данных
            await session.execute(
                Post.__table__.update()
                .values(posted=True)
                .where(Post.id == news_item.id)
            )
            await session.commit()


# Функция для периодической отправки новости каждый час
async def hourly_schedule():
    while True:
        await send_news()
        await asyncio.sleep(360)  # Подождать 1 час перед следующим запуском


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    loop.create_task(hourly_schedule())  # Запустить планировщик каждый час

    try:
        loop.run_until_complete(bot.send_message(chat_id=CHANNEL, text="Бот запущен!"))
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete(bot.send_message(chat_id=CHANNEL, text="Бот остановлен!"))
    finally:
        loop.run_until_complete(bot.session.close())
