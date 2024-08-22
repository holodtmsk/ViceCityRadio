from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Вставьте ваш токен здесь
BOT_TOKEN = 'ВАШ_ТОКЕН'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Логируем получение команды /start
    print("Получена команда /start")
    
    # Создаем кнопку, которая откроет ваше веб-приложение
    button = InlineKeyboardButton("Открыть Web App", web_app={"url": "https://instagram-bot22-1d84ba019e98.herokuapp.com"})
    keyboard = InlineKeyboardMarkup([[button]])

    # Отправляем сообщение с кнопкой
    await update.message.reply_text('Нажмите кнопку, чтобы открыть приложение:', reply_markup=keyboard)

# Создаем приложение Telegram Bot
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Добавляем обработчик команды /start
app.add_handler(CommandHandler("start", start))

# Запускаем бота
app.run_polling()


