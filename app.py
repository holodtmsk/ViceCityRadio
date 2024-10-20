import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

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
    category_name = " ".join(context.args)
    
    if not category_name:
        update.message.reply_text("Пожалуйста, укажите название категории.")
        return

    conn = sqlite3.connect('finance_bot.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO categories (name, user_id) VALUES (?, ?)", (category_name, user.id))
    conn.commit()
    conn.close()
    
    update.message.reply_text(f"Категория '{category_name}' добавлена.")

# Отображение кнопок категорий
def show_categories(update: Update, context):
    conn = sqlite3.connect('finance_bot.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM categories WHERE user_id = ?", (update.message.from_user.id,))
    categories = cursor.fetchall()

    if not categories:
        update.message.reply_text("Категорий пока нет. Используйте /addcategory для добавления.")
        return
    
    keyboard = [[InlineKeyboardButton(name, callback_data=str(category_id))] for category_id, name in categories]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text('Выберите категорию:', reply_markup=reply_markup)

# Обработка выбора категории и запись траты
def handle_category_selection(update: Update, context):
    query = update.callback_query
    query.answer()

    category_id = int(query.data)
    context.user_data['category_id'] = category_id
    query.edit_message_text(f"Вы выбрали категорию с ID: {category_id}. Введите сумму траты:")

# Обработка ввода суммы
def handle_message(update: Update, context):
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
    dp.add_handler(CallbackQueryHandler(handle_category_selection))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
