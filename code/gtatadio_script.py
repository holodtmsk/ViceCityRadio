from flask import Flask, render_template
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext

# Вставьте ваш токен здесь
BOT_TOKEN = '7503606129:AAEVHZPaRJhwRsPfAs2XrFDjybDSqHaS9_w'

app = Flask(__name__)

@app.route('/')
def index():
    # Это будет загружать файл index.html из директории templates
    return render_template('index.html')

async def start(update: Update, context: CallbackContext) -> None:
    # Создаем кнопку, которая откроет ваше веб-приложение
    button = InlineKeyboardButton("Open Web App", web_app={"url": "https://instagram-bot22-1d84ba019e98.herokuapp.com"})
    keyboard = InlineKeyboardMarkup([[button]])

    await update.message.reply_text('Click the button to open the app:', reply_markup=keyboard)

# Создаем приложение Telegram Bot
telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()

# Добавляем обработчик команды /start
telegram_app.add_handler(CommandHandler("start", start))

if __name__ == '__main__':
    # Запуск Flask приложения
    app.run(debug=True)

    # Запуск Telegram бота
    telegram_app.run_polling()
