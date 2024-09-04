from flask import Flask, request, jsonify

app = Flask(__name__)

# Пример базы данных пользователей (можно заменить на SQLite)
user_data = {
    "telegram_username": {
        "balance": 1000000000,
        "spins": 23,
        "history": []
    }
}

@app.route('/collect_reward', methods=['POST'])
def collect_reward():
    data = request.json
    username = data['username']
    spins_earned = data['spinsEarned']
    money_earned = data['moneyEarned']

    if username in user_data:
        user_data[username]['balance'] += money_earned
        user_data[username]['spins'] += spins_earned
        # Сохраняем историю
        user_data[username]['history'].append({
            'spins': spins_earned,
            'money': money_earned
        })

        return jsonify({
            'newBalance': user_data[username]['balance'],
            'newSpins': user_data[username]['spins']
        })

    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
