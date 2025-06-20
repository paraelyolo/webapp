from flask import Flask, render_template, redirect, session, request, url_for, jsonify
from werkzeug.security import check_password_hash
from utils.drive import descargar_csv_drive
import json
import os
import pandas as pd

app = Flask(__name__)
app.secret_key = 'superclave'  # cámbiala por una clave fuerte en producción

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(BASE_DIR, 'users.json')

CSV_IDS = {
    "operador": "1uIgigavolkY6xdWKw1DCEGmfsBD_wzn6",
    "horas_trabajo": "152IQbofX1hAKODLmOU8HJErDHW142hNH",
    "piezas_cortadas": "1EkZoRWAlvOMm9ED4cQJgmhAA_VAwOPi4",
    "tipo_perfil": "1Q6mnuyx80XRIohbxVu4cgimRyZP3J85A",
    "log": "1S7IvflfqXJURLwicx_wZUqpAP4opfht5"  # ✅ Nuevo ID de log
}

def obtener_valor_primera_celda(df):
    if df.empty:
        return "Sin datos"
    valor = df.iloc[0, 0]
    if pd.isna(valor):
        return "Sin datos"
    return str(valor)

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
    for clave in ["operador", "horas_trabajo", "piezas_cortadas", "tipo_perfil"]:
        file_id = CSV_IDS[clave]
        try:
            df = descargar_csv_drive(file_id)
            app.logger.info(f"Contenido CSV para {clave}: \n{df}")
            datos[clave] = obtener_valor_primera_celda(df)
        except Exception as e:
            error_msg = f"Error en '{clave}': {str(e)}"
            errores.append(error_msg)
            app.logger.error(error_msg)

    if errores:
        return "Errores detectados:<br>" + "<br>".join(errores), 500

    return render_template('dashboard.html', datos=datos)

@app.route('/api/datos')
def api_datos():
    if 'user' not in session:
        return jsonify({"error": "No autorizado"}), 401

    datos = {}
    for clave in ["operador", "horas_trabajo", "piezas_cortadas", "tipo_perfil"]:
        file_id = CSV_IDS[clave]
        try:
            df = descargar_csv_drive(file_id)
            datos[clave] = obtener_valor_primera_celda(df)
        except Exception as e:
            app.logger.error(f"Error al obtener {clave}: {e}")
            datos[clave] = "Error"

    return jsonify(datos)

@app.route('/log')
def log():
    if 'user' not in session:
        return redirect(url_for('login'))

    try:
        df_log = descargar_csv_drive(CSV_IDS["log"])
        registros = df_log.to_dict(orient='records')
    except Exception as e:
        app.logger.error(f"Error al cargar el log: {e}")
        registros = []

    return render_template('log.html', registros=registros, columnas=df_log.columns if not df_log.empty else [])

if __name__ == "__main__":
    app.run()
