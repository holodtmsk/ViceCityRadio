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

        return jsonify({
            'newBalance': balance,
            'newSpins': spins
        })
    else:
        return jsonify({'error': 'User not found'}), 404

# Обработка команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    url_button = telebot.types.InlineKeyboardButton(text="Open Web App", web_app=telebot.types.WebAppInfo(url="https://instagram-bot22-1d84ba019e98.herokuapp.com"))
    keyboard.add(url_button)
    bot.send_message(message.chat.id, "Click the button to open the app:", reply_markup=keyboard)


# Настройка вебхука
@app.route("/webhook", methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '!', 200


if __name__ == "__main__":
    # Инициализируем базу данных при запуске
    init_db()

    # Устанавливаем вебхук
    bot.remove_webhook()
    bot.set_webhook(url="https://instagram-bot22-1d84ba019e98.herokuapp.com/webhook")

    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
