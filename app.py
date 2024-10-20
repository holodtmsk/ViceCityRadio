from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

# Функция для старта, которая выводит кнопки
def start(update: Update, context):
    # Создаем кнопки
    keyboard = [
        [InlineKeyboardButton("Продукты", callback_data='1')],
        [InlineKeyboardButton("Кафе", callback_data='2')],
        [InlineKeyboardButton("Машина", callback_data='3')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Отправляем сообщение с кнопками
    update.message.reply_text('Выберите категорию:', reply_markup=reply_markup)

# Функция для обработки нажатий на кнопки
def button(update: Update, context):
    query = update.callback_query
    query.answer()
    
    # Обрабатываем нажатие в зависимости от callback_data
    if query.data == '1':
        query.edit_message_text(text="Вы выбрали Продукты.")
    elif query.data == '2':
        query.edit_message_text(text="Вы выбрали Кафе.")
    elif query.data == '3':
        query.edit_message_text(text="Вы выбрали Машина.")

# Основная функция запуска бота
def main():
    # Вставь сюда свой токен Telegram API
    updater = Updater("7726770034:AAE_X60ycvljNiGE-j0qLhjNaWZiPlpPRNU", use_context=True)

    dp = updater.dispatcher

    # Команда /start для вывода кнопок
    dp.add_handler(CommandHandler("start", start))
    
    # Обработчик нажатий на кнопки
    dp.add_handler(CallbackQueryHandler(button))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
