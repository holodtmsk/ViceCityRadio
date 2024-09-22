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

# Функция для добавления нового пользователя с начальными значениями
def add_user(username):
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (username, balance, spins, history)
        VALUES (?, ?, ?, ?)
    ''', (username, 1000, 5, ''))  # Начальный баланс 1000 и 5 спинов
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

# Функция для получения первой буквы имени
def get_initial(username):
    return username[0].upper()  # Первая буква имени капсом

# Маршрут для отображения главной страницы
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Получаем данные из POST-запроса
        data = request.json
        username = data.get('username')  # Имя пользователя, переданное через запрос

        if not username:
            return jsonify({'error': 'Username is missing'}), 400

        # Проверяем, есть ли пользователь в базе данных
        user = get_user(username)
        if not user:
            add_user(username)  # Если нет, создаем нового пользователя
            user = get_user(username)

        # Получаем первую букву имени (инициал)
        initial = get_initial(username)

        # Возвращаем HTML-страницу с балансом, количеством спинов и именем пользователя
        return render_template('index.html', balance=user[1], spins=user[2], username=username, initial=initial)
    
    elif request.method == 'GET':
        return render_template('index.html')

# Маршрут для сбора награды
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

# Настройка меню для запуска Mini App
def set_menu_button(chat_id):
    web_app_info = telebot.types.LoginUrl(url="https://instagram-bot22-1d84ba019e98.herokuapp.com")
    menu_button = telebot.types.MenuButtonWebApp(text="Open App", web_app=web_app_info)
    bot.set_chat_menu_button(chat_id=chat_id, menu_button=menu_button)

# Обработка команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        print(f"Processing /start for {message.chat.id}")
        
        keyboard = telebot.types.InlineKeyboardMarkup()
        url_button = telebot.types.InlineKeyboardButton(text="Open Web App", web_app=telebot.types.WebAppInfo(url="https://instagram-bot22-1d84ba019e98.herokuapp.com"))
        keyboard.add(url_button)
        
        bot.send_message(message.chat.id, "Click the button to open the app:", reply_markup=keyboard)
        print(f"Message sent to {message.chat.id}")
    except Exception as e:
        print(f"Error: {e}")

# Настройка вебхука
@app.route("/webhook", methods=['POST'])
def webhook():
    try:
        json_str = request.get_data().decode('UTF-8')
        print(f"Webhook data received: {json_str}")
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return '!', 200
    except Exception as e:
        print(f"Error processing webhook: {e}")
        return 'Error', 500

if __name__ == "__main__":
    init_db()
    bot.remove_webhook()
    bot.set_webhook(url="https://instagram-bot22-1d84ba019e98.herokuapp.com/webhook")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

