import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('finance_bot.db')
    cursor = conn.cursor()
    
    # Создание таблиц для категорий, трат и пользователей
    cursor.execute('''CREATE TABLE IF NOT EXISTS categories (
                        id INTEGER PRIMARY KEY, 
                        name TEXT, 
                        emoji TEXT, 
                        user_id INTEGER)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY, 
                        category_id INTEGER, 
                        amount REAL, 
                        date TEXT, 
                        user_id INTEGER)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY, 
                        username TEXT, 
                        is_admin INTEGER)''')
    
    conn.commit()
    conn.close()

# Функция для регистрации категории
def regkat(update: Update, context):
    user = update.message.from_user
    args = context.args
    if len(args) == 0:
        update.message.reply_text("Пожалуйста, укажите название категории.")
        return
    
    category_name = args[0]
    emoji = args[1] if len(args) > 1 else ""
    
    conn = sqlite3.connect('finance_bot.db')
    cursor = conn.cursor()
    
    # Вставка новой категории
    cursor.execute("INSERT INTO categories (name, emoji, user_id) VALUES (?, ?, ?)", (category_name, emoji, user.id))
    conn.commit()
    conn.close()
    
    update.message.reply_text(f"Категория {category_name} {emoji} добавлена!")

# Вывод кнопок с категориями
def show_categories(update: Update, context):
    conn = sqlite3.connect('finance_bot.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, emoji FROM categories WHERE user_id = ?", (update.message.from_user.id,))
    categories = cursor.fetchall()
    
    if not categories:
        update.message.reply_text("Категорий пока нет. Используйте /regkat для добавления.")
        return
    
    keyboard = []
    for category in categories:
        keyboard.append([InlineKeyboardButton(f"{category[1]} {category[2]}", callback_data=category[0])])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Выберите категорию:', reply_markup=reply_markup)

# Обработка нажатий на категории
def button_click(update: Update, context):
    query = update.callback_query
    query.answer()

    category_id = query.data
    context.user_data['category_id'] = category_id
    query.edit_message_text(text=f"Введите сумму для категории {category_id}:")
    
# Хендлер для ввода суммы
def handle_message(update: Update, context):
    user = update.message.from_user
    if 'category_id' not in context.user_data:
        update.message.reply_text("Пожалуйста, выберите категорию.")
        return
    
    try:
        amount = float(update.message.text)
    except ValueError:
        update.message.reply_text("Пожалуйста, введите корректную сумму.")
        return
    
    category_id = context.user_data['category_id']
    
    conn = sqlite3.connect('finance_bot.db')
    cursor = conn.cursor()
    
    # Добавление траты в базу данных
    cursor.execute("INSERT INTO expenses (category_id, amount, date, user_id) VALUES (?, ?, date('now'), ?)", (category_id, amount, user.id))
    conn.commit()
    conn.close()
    
    update.message.reply_text(f"Записано: {amount} руб.")
    del context.user_data['category_id']

# Отчеты по тратам за сегодня
def report_today(update: Update, context):
    user = update.message.from_user
    conn = sqlite3.connect('finance_bot.db')
    cursor = conn.cursor()

    cursor.execute("SELECT c.name, SUM(e.amount) FROM expenses e JOIN categories c ON e.category_id = c.id WHERE e.date = date('now') AND e.user_id = ? GROUP BY c.name", (user.id,))
    result = cursor.fetchall()

    if result:
        report = "\n".join([f"{row[0]}: {row[1]} руб." for row in result])
        update.message.reply_text(f"Отчёт за сегодня:\n{report}")
    else:
        update.message.reply_text("Сегодня трат не найдено.")

    conn.close()

# Основная функция запуска бота
def main():
    # Инициализация бота
    updater = Updater("7726770034:AAE_X60ycvljNiGE-j0qLhjNaWZiPlpPRNU", use_context=True)
    
    # Инициализация базы данных
    init_db()
    
    # Регистрация команд
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("regkat", regkat))
    dp.add_handler(CommandHandler("today", report_today))
    dp.add_handler(CommandHandler("categories", show_categories))
    dp.add_handler(CallbackQueryHandler(button_click))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
