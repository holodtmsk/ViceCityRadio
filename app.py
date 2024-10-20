from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Функция для старта, которая выводит кнопки снизу
def start(update: Update, context):
    # Создаем кнопки
    keyboard = [['Продукты', 'Кафе', 'Машина']]
    
    # Убираем one_time_keyboard, чтобы кнопки не пропадали
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    # Отправляем сообщение с кнопками
    update.message.reply_text('Выберите категорию:', reply_markup=reply_markup)

# Функция для обработки выбора
def button_response(update: Update, context):
    text = update.message.text

    if text == 'Продукты':
        update.message.reply_text("Вы выбрали Продукты.")
    elif text == 'Кафе':
        update.message.reply_text("Вы выбрали Кафе.")
    elif text == 'Машина':
        update.message.reply_text("Вы выбрали Машина.")
    else:
        update.message.reply_text("Выберите одну из предложенных категорий.")

# Основная функция запуска бота
def main():
    # Вставь сюда свой токен Telegram API
    updater = Updater("7726770034:AAE_X60ycvljNiGE-j0qLhjNaWZiPlpPRNU", use_context=True)

    dp = updater.dispatcher

    # Команда /start для вывода кнопок
    dp.add_handler(CommandHandler("start", start))
    
    # Обработчик выбора кнопки
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, button_response))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

