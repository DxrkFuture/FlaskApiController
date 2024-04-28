from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import psutil #статистика системы
from dotenv import load_dotenv
import os

# Загрузка переменных среды из файла .env
load_dotenv()
secret_key = os.getenv("SECRET_KEY")
user_names_str = os.getenv("USER_NAMES")

app = Flask(__name__)
app.secret_key = secret_key

users = {}
for user_info in user_names_str.split(","):
    username, password = user_info.split(":")
    users[username] = password

# print(users)

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username  # Сохраняем имя пользователя в сессии
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Неправильный логин или пароль")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

#  API SYSTEM
@app.route('/api/sysstats')
def get_system_stats():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent

    return jsonify({
        'cpu_usage': cpu_usage,
        'memory_usage': memory_usage,
        'disk_usage': disk_usage
    })

# END API SYSTEM

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)