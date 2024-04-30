from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_socketio import SocketIO, emit
import psutil #statistic system tool
from dotenv import load_dotenv
import subprocess
import gevent
import os


# Loading .env
load_dotenv()
secret_key = os.getenv("SECRET_KEY")
user_names_str = os.getenv("USER_NAMES")

app = Flask(__name__)
socketio = SocketIO(app)
app.secret_key = secret_key

users = {}
for user_info in user_names_str.split(","):
    username, password = user_info.split(":")
    users[username] = password

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
            session['username'] = username  # Save the user name in the session
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Неправильный логин или пароль")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

# Command System

@socketio.on('execute_command')
def handle_execute_command(command):
    global active_process
    try:
        # Set the UTF-8 encoding before executing the command
        subprocess.run(['chcp', '65001'], shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        emit('command_output', f"Error setting UTF-8 encoding: {e.output.decode('utf-8')}")
        return

    try:
        # Execute a custom command
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, text=True, encoding='UTF-8')
        active_process = process
        for line in process.stdout:
            emit('command_output', line.rstrip())
        process.stdout.close()
        return_code = process.wait()
        if return_code != 0:
            emit('command_output', f"Command execution failed with return code {return_code}.")
    except subprocess.CalledProcessError as e:
        emit('command_output', f"Error executing command: {e.output.decode('utf-8')}")

@socketio.on('stop_command')
def handle_stop_command():
    global active_process
    if active_process:
        active_process.terminate()  # stop the active process
        active_process.stdout.close()  # close the output stream
        active_process = None
        emit('command_output', 'Command stopped.')
    else:
        emit('command_output', 'No active command to stop.')

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
    socketio.run(app)
    app.run(debug=True)