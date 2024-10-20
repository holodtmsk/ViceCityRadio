import os
from telegram.ext import Updater, CommandHandler

# Функция для команды /start
def start(update, context):
    update.message.reply_text("Бот работает!")
    print("Команда /start выполнена")

# Функция для команды /help
def help_command(update, context):
    help_text = (
        "/regkat <название категории> [эмодзи] - добавить категорию\n"
        "/delkat <название категории> - удалить категорию и все траты по ней\n"
        "/transkat <из категории> to <в категорию> - перенести все траты из одной категории в другую\n"
        "/renamekat <старое название> to <новое название> - переименовать категорию\n"
        "/invite <@ник пользователя> - пригласить нового пользователя\n"
        "/today - отчёт по тратам за сегодня\n"
        "/week - отчёт по тратам за неделю\n"
        "/month - отчёт по тратам за месяц\n"
        "/date <дата> - отчёт по тратам за определённую дату\n"
        "/daterange <дата1> - <дата2> - отчёт по тратам за период\n"
        "/help - список всех команд"
    )
    update.message.reply_text(help_text)
    print("Команда /help выполнена")

def main():
    # Получаем токен и устанавливаем updater
    TOKEN = os.getenv('TELEGRAM_TOKEN', '7726770034:AAE_X60ycvljNiGE-j0qLhjNaWZiPlpPRNU')
    updater = Updater(TOKEN, use_context=True)

    # Регистрируем команды
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))

    # Запуск polling
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
