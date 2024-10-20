import logging
import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

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
    logger.info("Database initialized.")

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

    try:
        # Вставка новой категории
        cursor.execute("INSERT INTO categories (name, emoji, user_id) VALUES (?, ?, ?)", (category_name, emoji, user.id))
        conn.commit()
        update.message.reply_text(f"Категория {category_name} {emoji} добавлена!")
        logger.info(f"Категория '{category_name}' добавлена для пользователя {user.id}")
    except Exception as e:
        logger.error(f"Ошибка при добавлении категории: {e}")
        update.message.reply_text("Произошла ошибка при добавлении категории.")
    finally:
        conn.close()

    # Сразу показываем кнопки категорий
    show_categories(update, context)

# Отображение категорий в виде кнопок
def show_categories(update: Update, context):
    conn = sqlite3.connect('finance_bot.db')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, name, emoji FROM categories WHERE user_id = ?", (update.message.from_user.id,))
        categories = cursor.fetchall()
        logger.info(f"Категории для пользователя {update.message.from_user.id}: {categories}")
        
        if not categories:
            update.message.reply_text("Категорий пока нет. Используйте /regkat для добавления.")
            return

        keyboard = []
        for category in categories:
            keyboard.append([InlineKeyboardButton(f"{category[1]} {category[2]}", callback_data=category[0])])

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Выберите категорию:', reply_markup=reply_markup)
    except Exception as e:
        logger.error(f"Ошибка при отображении категорий: {e}")
        update.message.reply_text("Ошибка при отображении категорий.")
    finally:
        conn.close()

# Основная функция запуска бота
def main():
    updater = Updater("7726770034:AAE_X60ycvljNiGE-j0qLhjNaWZiPlpPRNU", use_context=True)
    init_db()

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("regkat", regkat))
    dp.add_handler(CallbackQueryHandler(num_keyboard_click))
    dp.add_handler(CommandHandler("categories", show_categories))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
