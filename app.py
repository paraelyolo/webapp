from flask import Flask, render_template, redirect, session, request, url_for
from werkzeug.security import check_password_hash
from utils.drive import descargar_csv_drive
import json
import os

app = Flask(__name__)
app.secret_key = 'superclave'  # cámbiala por una clave larga y única en producción

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(BASE_DIR, 'users.json')

# IDs de ejemplo — puedes luego hacer que dependan del usuario
CSV_IDS = {
    "operador": "1uIgigavolkY6xdWKw1DCEGmfsBD_wzn6",
    "horas_trabajo": "152IQbofX1hAKODLmOU8HJErDHW142hNH",
    "piezas_cortadas": "1EkZoRWAlvOMm9ED4cQJgmhAA_VAwOPi4",
    "tipo_perfil": "1Q6mnuyx80XRIohbxVu4cgimRyZP3J85A"
}

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']

    try:
        with open(USERS_FILE) as f:
            users = json.load(f)
    except Exception as e:
        return f"Error leyendo archivo de usuarios: {e}", 500

    user = users.get(username)
    if user and check_password_hash(user['password'], password):
        session['user'] = username
        return redirect(url_for('dashboard'))
    
    return "Login incorrecto", 401

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    datos = {}
    errores = []
    for clave, file_id in CSV_IDS.items():
        try:
            valor = descargar_csv_drive(file_id).iloc[0, 0]
            datos[clave] = valor
        except Exception as e:
            error_msg = f"Error en '{clave}': {str(e)}"
            errores.append(error_msg)
            app.logger.error(error_msg)

    if errores:
        return "Errores detectados:<br>" + "<br>".join(errores), 500

    return render_template('dashboard.html', datos=datos)

@app.route('/log')
def log():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('log.html')

if __name__ == "__main__":
    app.run()
