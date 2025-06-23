from flask import Blueprint, render_template, session, redirect, url_for, jsonify, current_app
from utils.drive import descargar_csv_drive
import os
import pandas as pd

dashboard_bp = Blueprint('dashboard', __name__)

CSV_IDS = {
    "operador": "1uIgigavolkY6xdWKw1DCEGmfsBD_wzn6",
    "horas_trabajo": "152IQbofX1hAKODLmOU8HJErDHW142hNH",
    "piezas_cortadas": "1EkZoRWAlvOMm9ED4cQJgmhAA_VAwOPi4",
    "tipo_perfil": "1Q6mnuyx80XRIohbxVu4cgimRyZP3J85A"
}

def obtener_valor_primera_celda(df):
    if df.empty or pd.isna(df.iloc[0, 0]):
        return "Sin datos"
    return str(df.iloc[0, 0])

@dashboard_bp.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login.login'))

    datos = {}
    errores = []
    for clave in CSV_IDS:
        try:
            df = descargar_csv_drive(CSV_IDS[clave], con_encabezado=False)
            datos[clave] = obtener_valor_primera_celda(df)
        except Exception as e:
            current_app.logger.error(f"Error al obtener {clave}: {e}")
            datos[clave] = "Error"
            errores.append(str(e))
    return render_template("dashboard.html", datos=datos)

@dashboard_bp.route('/api/datos')
def api_datos():
    if 'user' not in session:
        return jsonify({"error": "No autorizado"}), 401

    datos = {}
    for clave in CSV_IDS:
        try:
            df = descargar_csv_drive(CSV_IDS[clave], con_encabezado=False)
            datos[clave] = obtener_valor_primera_celda(df)
        except Exception as e:
            current_app.logger.error(f"Error en API {clave}: {e}")
            datos[clave] = "Error"
    return jsonify(datos)
