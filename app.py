from telegram.ext import Updater, CommandHandler

# Простейшая функция, реагирующая на команду /start
def start(update, context):
    update.message.reply_text("Бот работает!")

def main():
    # Инициализация бота
    updater = Updater("7726770034:AAE_X60ycvljNiGE-j0qLhjNaWZiPlpPRNU", use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
