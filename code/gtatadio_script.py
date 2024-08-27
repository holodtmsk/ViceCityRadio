from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/collect_reward')
def collect_reward():
    return "Reward collected!"

if __name__ == "__main__":
    app.run(debug=True)
