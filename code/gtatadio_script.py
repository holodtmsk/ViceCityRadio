from flask import Flask, render_template
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from threading import Thread
import os

# Вставьте ваш токен здесь
BOT_TOKEN = '7503606129:AAEVHZPaRJhwRsPfAs2XrFDjybDSqHaS9_w'

# Создание Flask приложения
app = Flask(__name__)

@app.route('/')
def index():
    # Это будет загружать файл index.html из директории templates
    return render_template('index.html')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Создаем кнопку, которая откроет ваше веб-приложение
    button = InlineKeyboardButton("Open Web App", url="https://instagram-bot22-1d84ba019e98.herokuapp.com")
    keyboard = InlineKeyboardMarkup([[button]])

    await update.message.reply_text('Click the button to open the app:', reply_markup=keyboard)

# Создание и настройка Telegram Bot приложения
def run_telegram_bot():
    telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Добавляем обработчик команды /start
    telegram_app.add_handler(CommandHandler("start", start))

    # Запуск Telegram бота
    telegram_app.run_polling()

if __name__ == '__main__':
    # Запуск Telegram бота в отдельном потоке
    bot_thread = Thread(target=run_telegram_bot)
    bot_thread.start()

    # Запуск Flask приложения
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), use_reloader=False)
