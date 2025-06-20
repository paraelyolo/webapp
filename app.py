from flask import Flask, render_template, redirect, session, request, url_for
from werkzeug.security import check_password_hash
from utils.drive import descargar_csv_drive
import json
import os

app = Flask(__name__)
app.secret_key = 'superclave'  # cámbiala por una clave larga y única en producción

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(BASE_DIR, 'users.json')

# Página de login
@app.route('/')
def login():
    return render_template('login.html')

# Procesa el formulario de login
@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']

    try:
        with open(USERS_FILE) as f:
            users = json.load(f)
    except Exception:
        return "Error leyendo archivo de usuarios.", 500

    user = users.get(username)
    if user and check_password_hash(user['password'], password):
        session['user'] = username
        return redirect(url_for('dashboard'))
    
    return "Login incorrecto", 401

# Dashboard con la lista de máquinas
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    # Aquí iría la lógica para mostrar datos desde csv, por ahora renderizamos plantilla
    return render_template('dashboard.html')

# Página de logs, accesible desde el botón LOG
@app.route('/log')
def log():
    if 'user' not in session:
        return redirect(url_for('login'))
    # Aquí cargarías y mostrarías el CSV histórico
    return render_template('log.html')

if __name__ == "__main__":
    app.run()

