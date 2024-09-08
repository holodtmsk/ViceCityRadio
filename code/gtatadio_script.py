from flask import Flask, render_template, request, jsonify
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CommandHandler, CallbackContext
import telebot
import sqlite3
import os

app = Flask(__name__)
bot = telebot.TeleBot("7503606129:AAEVHZPaRJhwRsPfAs2XrFDjybDSqHaS9_w")

# Удаляем вебхук, если он установлен
bot.remove_webhook()

# Обработка команды start
def start(update: Update, context: CallbackContext):
    # URL на ваше Telegram Mini App
    mini_app_url = 'https://t.me/ViceCityRadioBot?start=mini_app'

    # Формируем кнопку для открытия мини-приложения
    keyboard = [
        [InlineKeyboardButton("Open Mini App", url=mini_app_url)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправляем сообщение с кнопкой пользователю
    update.message.reply_text('Welcome! Click the button below to open the Mini App:', reply_markup=reply_markup)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            balance INTEGER NOT NULL,
            spins INTEGER NOT NULL,
            history TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Функция для добавления нового пользователя
def add_user(username):
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (username, balance, spins, history)
        VALUES (?, ?, ?, ?)
    ''', (username, 0, 0, ''))
    conn.commit()
    conn.close()

# Функция для получения данных пользователя
def get_user(username):
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user

# Функция для обновления данных пользователя
def update_user(username, new_balance, new_spins, history):
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users SET balance = ?, spins = ?, history = ? WHERE username = ?
    ''', (new_balance, new_spins, history, username))
    conn.commit()
    conn.close()

# Функция для получения инициалов (первые 2 буквы)
def get_initials(username):
    return username[:2].upper()

@app.route('/')
def index():
    # Замените "telegram_username" на реальное имя пользователя из Telegram
    username = "kholodvlad"  # Пример имени, вместо этого используйте реальное имя пользователя из Telegram
    
    user = get_user(username)
    if not user:
        add_user(username)
        user = get_user(username)

    # Получаем инициалы
    initials = get_initials(username)

    # Передаем имя пользователя, баланс, спины и инициалы в шаблон для рендеринга
    return render_template('index.html', balance=user[1], spins=user[2], username=username, initials=initials)

@app.route('/collect_reward', methods=['POST'])
def collect_reward():
    data = request.json
    username = data.get('username')

    # Проверка наличия имени пользователя
    if not username:
        return jsonify({'error': 'Username is missing'}), 400

    spins_earned = 3  # Количество спинов, которые зарабатывает пользователь
    money_earned = 1000  # Сумма денег, которую зарабатывает пользователь

    # Получаем данные пользователя
    user = get_user(username)
    
    if user:
        balance = user[1] + money_earned
        spins = user[2] + spins_earned
        history = user[3] + f"Earned {money_earned} and {spins_earned} spins. "

        # Обновляем данные пользователя
        update_user(username, balance, spins, history)

        return jsonify({
            'newBalance': balance,
            'newSpins': spins
        })
    else:
        return jsonify({'error': 'User not found'}), 404

@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    url_button = telebot.types.InlineKeyboardButton(text="Open Web App", url="https://your-app-url.com")
    keyboard.add(url_button)
    bot.send_message(message.chat.id, "Click the button to open the app:", reply_markup=keyboard)

if __name__ == "__main__":
    # Инициализируем базу данных при запуске
    init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
