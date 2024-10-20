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
    
    # Сразу показываем кнопки категорий
    show_categories(update, context)

# Удаление категории и всех трат по ней
def delkat(update: Update, context):
    user = update.message.from_user
    args = context.args
    if len(args) == 0:
        update.message.reply_text("Пожалуйста, укажите название категории.")
        return
    
    category_name = " ".join(args).strip()
    
    conn = sqlite3.connect('finance_bot.db')
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM categories WHERE TRIM(name) = ? AND user_id = ?", (category_name, user.id))
    category = cursor.fetchone()

    if category:
        category_id = category[0]
        cursor.execute("DELETE FROM expenses WHERE category_id = ?", (category_id,))
        cursor.execute("DELETE FROM categories WHERE id = ?", (category_id,))
        conn.commit()
        update.message.reply_text(f"Категория {category_name} и все связанные с ней траты удалены.")
    else:
        update.message.reply_text("Категория не найдена.")
    
    conn.close()

# Переименование категории
def renamekat(update: Update, context):
    user = update.message.from_user
    args = context.args
    if len(args) < 3 or args[1].lower() != "to":
        update.message.reply_text("Использование: /renamekat <старое название> to <новое название>")
        return
    
    old_name = args[0]
    new_name = args[2]
    
    conn = sqlite3.connect('finance_bot.db')
    cursor = conn.cursor()
    
    cursor.execute("UPDATE categories SET name = ? WHERE name = ? AND user_id = ?", (new_name, old_name, user.id))
    conn.commit()
    
    if cursor.rowcount > 0:
        update.message.reply_text(f"Категория {old_name} переименована в {new_name}.")
    else:
        update.message.reply_text("Категория не найдена.")
    
    conn.close()

# Отображение категорий в виде кнопок
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

# Числовая клавиатура для ввода суммы
def show_num_keyboard(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("1", callback_data="1"), InlineKeyboardButton("2", callback_data="2"), InlineKeyboardButton("3", callback_data="3")],
        [InlineKeyboardButton("4", callback_data="4"), InlineKeyboardButton("5", callback_data="5"), InlineKeyboardButton("6", callback_data="6")],
        [InlineKeyboardButton("7", callback_data="7"), InlineKeyboardButton("8", callback_data="8"), InlineKeyboardButton("9", callback_data="9")],
        [InlineKeyboardButton(".", callback_data="."), InlineKeyboardButton("0", callback_data="0"), InlineKeyboardButton("C", callback_data="clear")],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Введите сумму:', reply_markup=reply_markup)

# Обработка нажатий на клавиатуру
def num_keyboard_click(update: Update, context):
    query = update.callback_query
    query.answer()

    current_sum = context.user_data.get('sum', "")
    
    if query.data == "clear":
        current_sum = ""  # Сброс суммы
    else:
        current_sum += query.data  # Добавляем цифру

    context.user_data['sum'] = current_sum
    query.edit_message_text(text=f"Введите сумму: {current_sum}")

# Запись траты и вывод отчета
def handle_expense(update: Update, context):
    user = update.message.from_user
    category_id = context.user_data.get('category_id', None)
    sum_amount = context.user_data.get('sum', None)

    if not category_id or not sum_amount:
        update.message.reply_text("Пожалуйста, выберите категорию и введите сумму.")
        return

    conn = sqlite3.connect('finance_bot.db')
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO expenses (category_id, amount, date, user_id) VALUES (?, ?, date('now'), ?)", (category_id, sum_amount, user.id))
    conn.commit()
    
    context.user_data['sum'] = ""
    
    update.message.reply_text(f"Записано: {sum_amount} руб. на {category_id}")
    
    report_today(update, context)
    conn.close()

# Отчет за сегодня
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
    updater = Updater("7726770034:AAE_X60ycvljNiGE-j0qLhjNaWZiPlpPRNU", use_context=True)
    init_db()

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("regkat", regkat))
    dp.add_handler(CommandHandler("delkat", delkat))
    dp.add_handler(CommandHandler("renamekat", renamekat))
    dp.add_handler(CommandHandler("today", report_today))
    dp.add_handler(CallbackQueryHandler(num_keyboard_click))
    dp.add_handler(CommandHandler("categories", show_categories))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
