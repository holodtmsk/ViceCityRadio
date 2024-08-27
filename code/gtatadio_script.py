from flask import Flask, render_template, request
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
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
    keyboard = InlineKeyboardMarkup()
    url_button = InlineKeyboardButton(text="Open Web App", url="https://instagram-bot22-1d84ba019e98.herokuapp.com")
    keyboard.add(url_button)
    bot.send_message(message.chat.id, "Click the button to open the app:", reply_markup=keyboard)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
