from flask import Flask, render_template, redirect, session, request, url_for
from werkzeug.security import check_password_hash
from utils.drive import descargar_csv_drive
import json

app = Flask(__name__)
app.secret_key = 'superclave'  # cámbiala por una clave larga y única en producción

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
        with open('users.json') as f:
            users = json.load(f)
    except Exception:
        return "Error leyendo archivo de usuarios.", 500

    user = users.get(username)
    if user and check_password_hash(user['password'], password):
        session['user'] = username
        return redirect(url_for('dashboard'))
    
    return "Login incorrecto", 401


# Aquí irían las otras rutas, ej dashboard, log, etc.

if __name__ == "__main__":
    app.run()

