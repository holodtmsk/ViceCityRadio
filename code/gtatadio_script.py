from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext

# Вставьте ваш токен здесь
BOT_TOKEN = '7503606129:AAEVHZPaRJhwRsPfAs2XrFDjybDSqHaS9_w'

async def start(update: Update, context: CallbackContext) -> None:
    # Создаем кнопку, которая откроет ваше веб-приложение
    button = InlineKeyboardButton("Open Web App", web_app={"url": "https://instagram-bot22-1d84ba019e98.herokuapp.com"})
    keyboard = InlineKeyboardMarkup([[button]])

    await update.message.reply_text('Click the button to open the app:', reply_markup=keyboard)

# Создаем приложение Telegram Bot
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Добавляем обработчик команды /start
app.add_handler(CommandHandler("start", start))

# Запускаем бота
app.run_polling()
