from flask import Flask, render_template, request, session, redirect
import json

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# A temporary dictionary to hold user data (use a database in production)
user_data = {}

@app.route('/')
def index():
    username = session.get('username', 'guest')
    if username not in user_data:
        user_data[username] = {'balance': 0, 'spins': 0}
    return render_template('index.html', balance=user_data[username]['balance'], spins=user_data[username]['spins'])

@app.route('/start_farming')
def start_farming():
    # This would normally trigger farming logic
    username = session.get('username', 'guest')
    if username in user_data:
        # Simulate earning spins and money
        user_data[username]['spins'] += 10
        user_data[username]['balance'] += 1000
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    session['username'] = request.form['username']
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

