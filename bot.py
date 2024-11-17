from flask import Flask
from threading import Thread
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from handlers import start, handle_message, broadcast_message

# Telegram Bot Token из переменных окружения
import os
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not TOKEN:
    raise ValueError("Bot token not found. Please set TELEGRAM_BOT_TOKEN as an environment variable.")

# Flask-приложение для проверки доступности
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running", 200

def run_flask():
    # Flask будет слушать запросы на порту 5000
    app.run(host="0.0.0.0", port=5000)

def main():
    # Telegram Bot Setup
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Регистрация обработчиков
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("broadcast", broadcast_message))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Запуск Telegram-бота
    updater.start_polling()

    # Запуск Flask-сервера в отдельном потоке
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # Ожидание завершения работы бота
    updater.idle()

if __name__ == "__main__":
    main()
