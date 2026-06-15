import asyncio
import os
import aiohttp
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from main.hendlers import router as hendlers_router
from database import init_answer, init_play  

async def pinger():
    """Функция, которая каждые 10 минут пингует сервер, чтобы бот не засыпал"""
    await asyncio.sleep(15)
    
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.get('https://telegramm-bot-rpin.onrender.com') as response:
                    print(f"[Self-Ping] Статус веб-сайта: {response.status}")
                
            except Exception as e:
                print(f"[Self-Ping] Ошибка авто-пина: {e}")
            
            await asyncio.sleep(600)

load_dotenv()
token = os.getenv("TOKEN")

dp = Dispatcher()
dp.include_router(hendlers_router)

async def main():
    bot = Bot(token)
    print("Инициализация таблиц базы данных...")
    await init_answer() 
    await init_play()   
    print("Все таблицы успешно созданы и готовы к работе!")
    
    asyncio.create_task(pinger())
    
    print("Бот успешно запущен, пингер работает!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен!")
