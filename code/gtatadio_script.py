from flask import Flask, render_template, request
import telebot

app = Flask(__name__)
bot = telebot.TeleBot("7503606129:AAEVHZPaRJhwRsPfAs2XrFDjybDSqHaS9_w")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/collect_reward')
def collect_reward():
    return "Reward collected!"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the game! Visit the web page to play.")

if __name__ == "__main__":
    bot.polling(none_stop=True)
    app.run(debug=True)
