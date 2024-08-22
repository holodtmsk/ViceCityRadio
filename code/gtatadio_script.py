from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext

app = Flask(__name__)

BOT_TOKEN = '7503606129:AAEVHZPaRJhwRsPfAs2XrFDjybDSqHaS9_w'

async def start(update: Update, context: CallbackContext) -> None:
    button = InlineKeyboardButton("Open Web App", web_app={"url": "https://ваш-домен.herokuapp.com"})
    keyboard = InlineKeyboardMarkup([[button]])
    await update.message.reply_text('Click the button to open the app:', reply_markup=keyboard)

telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()
telegram_app.add_handler(CommandHandler("start", start))

@app.route('/' + BOT_TOKEN, methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    telegram_app.process_update(update)
    return 'ok'

if __name__ == "__main__":
    app.run()
