from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import MessageHandler
from bot_manager import BotManager
from scraping_scheduler import ScrapingScheduler

async def on_startup(dp, bot, chat_id):
    await bot.send_message(chat_id, 'Bot has been started')

async def on_shutdown(dp, bot, chat_id):
    await bot.send_message(chat_id, 'Bot has been stopped')

def main():
    manager = BotManager()
    TOKEN = ''
    
    bot = Bot(token=TOKEN)
    dp = Dispatcher(bot)

    # Command handlers
    dp.register_message_handler(manager.start, content_types=types.ContentType.COMMAND, commands=['start'])
    dp.register_message_handler(manager.setup, content_types=types.ContentType.COMMAND, commands=['setup'])
    dp.register_message_handler(manager.help, content_types=types.ContentType.COMMAND, commands=['help'])
    dp.register_message_handler(manager.handle_message, MessageHandler)

    # For the scraping scheduler
    scheduler = ScrapingScheduler(manager)

    # Start the bot and the scheduler
    from aiogram import executor
    executor.start_polling(dp, on_startup=lambda dp: on_startup(dp, bot), on_shutdown=lambda dp: on_shutdown(dp, bot))
    scheduler.start()

if __name__ == '__main__':
    main()