from flask import Flask, render_template, request, jsonify
import telebot
import sqlite3
import os

app = Flask(__name__)
bot = telebot.TeleBot("7503606129:AAEVHZPaRJhwRsPfAs2XrFDjybDSqHaS9_w")

# Удаляем вебхук, если он установлен
bot.remove_webhook()

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

# Обработчик команды /start с клавиатурой
@bot.message_handler(commands=['start'])
def start(message):
    # Создаём клавиатуру с кнопками "Web App" и "Help"
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton("Web App")
    btn2 = telebot.types.KeyboardButton("Help")
    keyboard.add(btn1, btn2)
    bot.send_message(message.chat.id, "Select an option:", reply_markup=keyboard)

# Обработчик для кнопки "Web App"
@bot.message_handler(func=lambda message: message.text == "Web App")
def send_web_app(message):
    # Отправляем ссылку на веб-приложение
    bot.send_message(message.chat.id, "Here is your web app link: https://your-app-url.com")

# Обработчик для кнопки "Help"
@bot.message_handler(func=lambda message: message.text == "Help")
def send_help(message):
    # Отправляем сообщение помощи
    bot.send_message(message.chat.id, "Here is how to use the bot...")

@app.route('/')
def index():
    username = "kholodvlad"  # Пример имени, вместо этого используйте реальное имя пользователя из Telegram
    user = get_user(username)
    if not user:
        add_user(username)
        user = get_user(username)

    initials = get_initials(username)
    return render_template('index.html', balance=user[1], spins=user[2], username=username, initials=initials)

@app.route('/collect_reward', methods=['POST'])
def collect_reward():
    data = request.json
    username = data.get('username')

    if not username:
        return jsonify({'error': 'Username is missing'}), 400

    spins_earned = 3
    money_earned = 1000

    user = get_user(username)
    if user:
        balance = user[1] + money_earned
        spins = user[2] + spins_earned
        history = user[3] + f"Earned {money_earned} and {spins_earned} spins. "
        update_user(username, balance, spins, history)
        return jsonify({'newBalance': balance, 'newSpins': spins})
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

