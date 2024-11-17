import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from handlers import start, handle_message, broadcast_message, send_detailed_stats_to_admin

# Загрузка переменной окружения для токена
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not TOKEN:
    raise ValueError("Bot token not found. Please set TELEGRAM_BOT_TOKEN as an environment variable.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Регистрация обработчиков
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("broadcast", broadcast_message))
    dp.add_handler(CommandHandler("stats", send_detailed_stats_to_admin))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
