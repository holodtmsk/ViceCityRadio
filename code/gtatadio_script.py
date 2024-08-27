from flask import Flask, render_template, request
import telebot
import threading
import os

app = Flask(__name__)
bot = telebot.TeleBot("7503606129:AAEVHZPaRJhwRsPfAs2XrFDjybDSqHaS9_w")

# Удаляем вебхук, если он установлен
bot.remove_webhook()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/collect_reward')
def collect_reward():
    return "Reward collected!"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Используем Markdown для форматирования ссылки
    bot.reply_to(message, "Welcome to the game! [Visit the web page to play](https://instagram-bot22-1d84ba019e98.herokuapp.com).")

def run_bot():
    bot.polling(non_stop=True)

if __name__ == "__main__":
    # Запускаем бота в отдельном потоке
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()

    # Запускаем Flask-приложение
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
