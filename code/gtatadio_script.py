from telegram.ext import ApplicationBuilder, CommandHandler
import os

# Вставьте ваш токен здесь
BOT_TOKEN = '7503606129:AAEVHZPaRJhwRsPfAs2XrFDjybDSqHaS9_w'

# Функция для обработки команды /start
async def start(update, context):
    await update.message.reply_text('Hello!')

# Создание приложения Telegram Bot
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Добавляем обработчик команды /start
app.add_handler(CommandHandler("start", start))

# Настройка Webhook
PORT = int(os.environ.get('PORT', '8443'))
app.run_webhook(
    listen="0.0.0.0",
    port=PORT,
    url_path=BOT_TOKEN,
    webhook_url=f"https://{os.environ.get('HEROKU_APP_NAME')}.herokuapp.com/{BOT_TOKEN}"
)

