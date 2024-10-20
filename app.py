import sqlite3
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('finance_bot.db')
    cursor = conn.cursor()
    
    # Создание таблиц для категорий и трат
    cursor.execute('''CREATE TABLE IF NOT EXISTS categories (
                        id INTEGER PRIMARY KEY, 
                        name TEXT, 
                        user_id INTEGER)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY, 
                        category_id INTEGER, 
                        amount REAL, 
                        date TEXT, 
                        user_id INTEGER)''')
    
    conn.commit()
    conn.close()

# Регистрация новой категории
def add_category(update: Update, context):
    user = update.message.from_user
    category_name = " ".join(context.args).strip().lower()
    
    if not category_name:
        update.message.reply_text("Пожалуйста, укажите название категории.")
        return

    conn = sqlite3.connect('finance_bot.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO categories (name, user_id) VALUES (?, ?)", (category_name, user.id))
    conn.commit()
    conn.close()
    
    update.message.reply_text(f"Категория '{category_name}' добавлена.")

# Отображение кнопок категорий внизу
def show_categories(update: Update, context):
    conn = sqlite3.connect('finance_bot.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM categories WHERE user_id = ?", (update.message.from_user.id,))
    categories = cursor.fetchall()

    if not categories:
        update.message.reply_text("Категорий пока нет. Используйте /addcategory для добавления.")
        return

    # Формируем список кнопок для каждой категории
    category_buttons = [[category[0].capitalize()] for category in categories]  # Добавлено приведение к заглавной букве
    
    reply_markup = ReplyKeyboardMarkup(category_buttons, one_time_keyboard=False, resize_keyboard=True)
    update.message.reply_text('Выберите категорию:', reply_markup=reply_markup)

# Обработка выбора категории и запись траты
def handle_expense(update: Update, context):
    user = update.message.from_user
    category_name = update.message.text.lower()  # Приведение текста к нижнему регистру

    # Ищем категорию в базе данных
    conn = sqlite3.connect('finance_bot.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM categories WHERE LOWER(name) = ? AND user_id = ?", (category_name, user.id))  # Приведение имени к нижнему регистру
    category = cursor.fetchone()

    if not category:
        update.message.reply_text("Такой категории не существует. Пожалуйста, выберите существующую категорию.")
        return

    # Запрашиваем сумму траты
    context.user_data['category_id'] = category[0]
    update.message.reply_text(f"Введите сумму для категории '{category_name}'.")

# Обработка суммы и запись траты в базу данных
def handle_amount(update: Update, context):
    user = update.message.from_user
    category_id = context.user_data.get('category_id')

    if not category_id:
        update.message.reply_text("Пожалуйста, сначала выберите категорию.")
        return

    try:
        amount = float(update.message.text)
    except ValueError:
        update.message.reply_text("Пожалуйста, введите корректную сумму.")
        return

    conn = sqlite3.connect('finance_bot.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (category_id, amount, date, user_id) VALUES (?, ?, date('now'), ?)",
                   (category_id, amount, user.id))
    conn.commit()
    conn.close()

    update.message.reply_text(f"Трата {amount} записана.")

# Основная функция запуска бота
def main():
    updater = Updater("7726770034:AAE_X60ycvljNiGE-j0qLhjNaWZiPlpPRNU", use_context=True)
    init_db()

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", show_categories))
    dp.add_handler(CommandHandler("addcategory", add_category))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_expense))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_amount))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
