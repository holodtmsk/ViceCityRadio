from flask import Flask, render_template, request, jsonify
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

app = Flask(__name__)
bot = telebot.TeleBot("7503606129:AAEVHZPaRJhwRsPfAs2XrFDjybDSqHaS9_w")

# Пример базы данных пользователей (в памяти, можно заменить на SQLite)
user_data = {
    "telegram_username": {
        "balance": 1000000000,
        "spins": 23,
        "history": []
    }
}

# Удаляем вебхук, если он установлен
bot.remove_webhook()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/collect_reward', methods=['POST'])
def collect_reward():
    data = request.json
    username = data['username']
    spins_earned = data['spinsEarned']
    money_earned = data['moneyEarned']

    # Обновляем данные пользователя
    if username in user_data:
        user_data[username]['balance'] += money_earned
        user_data[username]['spins'] += spins_earned
        user_data[username]['history'].append({
            'spins': spins_earned,
            'money': money_earned
        })
        return jsonify({
            'newBalance': user_data[username]['balance'],
            'newSpins': user_data[username]['spins']
        })
    return jsonify({'error': 'User not found'}), 404

@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = InlineKeyboardMarkup()
    url_button = InlineKeyboardButton(text="Open Web App", url="https://your-app-url.com")
    keyboard.add(url_button)
    bot.send_message(message.chat.id, "Click the button to open the app:", reply_markup=keyboard)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
