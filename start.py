import asyncio
import os
import aiohttp
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from main.hendlers import router as hendlers_router
from main.hendlers_python import router as hendlers_router_python
from main.hendlers_robotics import router as hendlers_router_robotics
from main.command import router as command_router
from main.play1 import router as play_router
from main.play2 import router as play2_router
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
dp.include_router(hendlers_router,
                 hendlers_router_python,
                 hendlers_router_robotics,
                 command_router,
                 play_router,
                 play2_router,)

async def main():
    bot = Bot(token)
    print("Инициализация таблиц базы данных...")
    await init_answer() 
    await init_play()   
    print("Все таблицы успешно созданы и готовы к работе!")
    app = aiohttp.web.Application()
    app.router.add_get('/', handle)
    runner = aiohttp.web.AppRunner(app)
    await runner.setup()
    
    # Рендер автоматически передает номер порта в переменную окружения PORT.
    # Если ее нет, используем стандартный порт 10000.
    port = int(os.getenv("PORT", 10000))
    site = aiohttp.web.TCPSite(runner, '0.0.0.0', port)
    
    # Запускаем микро-сайт в фоне
    asyncio.create_task(site.start())
    print(f"Микро-веб-сервер запущен на порту {port}!")
    asyncio.create_task(pinger())
    
    print("Бот успешно запущен, пингер работает!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен!")
