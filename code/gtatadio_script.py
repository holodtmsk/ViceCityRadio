from flask import Flask, render_template
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext, ContextTypes

# Вставьте ваш токен здесь
BOT_TOKEN = '7503606129:AAEVHZPaRJhwRsPfAs2XrFDjybDSqHaS9_w'

# Создание Flask приложения
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', 
                           emotion_url='https://disk.yandex.ru/d/U3nGEWXN06uuYg',
                           vrock_url='https://disk.yandex.ru/d/NSofbwMSIUqSdA',
                           wave_url='https://disk.yandex.ru/d/WjhlOGNdtCbA5w')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    button = InlineKeyboardButton("Open Web App", url="https://instagram-bot22.herokuapp.com")
    keyboard = InlineKeyboardMarkup([[button]])

    await update.message.reply_text('Click the button to open the app:', reply_markup=keyboard)

# Создаем приложение Telegram Bot
telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()

# Добавляем обработчик команды /start
telegram_app.add_handler(CommandHandler("start", start))

if __name__ == '__main__':
    # Запуск Flask приложения
    app.run(debug=True, use_reloader=False)

    # Запуск Telegram бота
    telegram_app.run_polling()

