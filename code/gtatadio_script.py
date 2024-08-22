from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext

# Вставьте ваш токен здесь
BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

async def start(update: Update, context: CallbackContext) -> None:
    # Создаем кнопку, которая откроет ваше веб-приложение
    button = InlineKeyboardButton("Open Web App", web_app={"url": "https://your-app-name.herokuapp.com"})
    keyboard = InlineKeyboardMarkup([[button]])

    await update.message.reply_text('Click the button to open the app:', reply_markup=keyboard)

# Создаем приложение Telegram Bot
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Добавляем обработчик команды /start
app.add_handler(CommandHandler("start", start))

# Запускаем бота
app.run_polling()
