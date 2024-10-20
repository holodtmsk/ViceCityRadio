import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, Heroku!"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

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
                        user_id INTEGER)''')
    
    conn.commit()
    conn.close()

# Функция для отображения категорий
def show_categories(update: Update, context):
    conn = sqlite3.connect('finance_bot.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM categories WHERE user_id = ?", (update.message.from_user.id,))
    categories = cursor.fetchall()
    
    if not categories:
        update.message.reply_text("Категорий пока нет. Используйте /addcategory для добавления.")
        return
    
    keyboard = []
    for category in categories:
        keyboard.append([InlineKeyboardButton(category[1], callback_data=str(category[0]))])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Выберите категорию:', reply_markup=reply_markup)

# Функция для добавления новой категории
def add_category(update: Update, context):
    user = update.message.from_user
    args = context.args
    if len(args) == 0:
        update.message.reply_text("Пожалуйста, укажите название категории.")
        return
    
    category_name = args[0]
    
    conn = sqlite3.connect('finance_bot.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO categories (name, user_id) VALUES (?, ?)", (category_name, user.id))
    conn.commit()
    conn.close()
    
    update.message.reply_text(f"Категория {category_name} добавлена!")

# Обработка выбора категории и ввода суммы
def handle_category_selection(update: Update, context):
    query = update.callback_query
    query.answer()

    # Сохраняем выбранную категорию в контексте
    context.user_data['selected_category'] = query.data
    update.callback_query.message.reply_text("Введите сумму:")

# Обработка ввода суммы
def handle_message(update: Update, context):
    user = update.message.from_user
    selected_category = context.user_data.get('selected_category')
    
    if selected_category:
        try:
            amount = float(update.message.text)
        except ValueError:
            update.message.reply_text("Пожалуйста, введите правильную сумму.")
            return
        
        conn = sqlite3.connect('finance_bot.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO expenses (category_id, amount, user_id) VALUES (?, ?, ?)", (selected_category, amount, user.id))
        conn.commit()
        conn.close()
        
        update.message.reply_text(f"Записано: {amount} на категорию {selected_category}")
        
        # Отобразить текущие траты
        show_current_expenses(update, context)
    else:
        update.message.reply_text("Пожалуйста, выберите категорию для записи траты с помощью кнопок.")

# Показ текущих расходов по категориям
def show_current_expenses(update: Update, context):
    user = update.message.from_user
    conn = sqlite3.connect('finance_bot.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT c.name, SUM(e.amount) 
                      FROM expenses e 
                      JOIN categories c ON e.category_id = c.id 
                      WHERE e.user_id = ? 
                      GROUP BY c.name''', (user.id,))
    result = cursor.fetchall()

    if result:
        report = "\n".join([f"{row[0]}: {row[1]} руб." for row in result])
        update.message.reply_text(f"Текущие расходы:\n{report}")
    else:
        update.message.reply_text("Пока нет записанных трат.")
    
    conn.close()

# Основная функция запуска бота
def main():
    updater = Updater("7726770034:AAE_X60ycvljNiGE-j0qLhjNaWZiPlpPRNU", use_context=True)
    init_db()

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("addcategory", add_category))
    dp.add_handler(CommandHandler("categories", show_categories))
    dp.add_handler(CallbackQueryHandler(handle_category_selection))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
