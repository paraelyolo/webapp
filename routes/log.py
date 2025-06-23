from flask import Blueprint, render_template, jsonify, session, current_app
from utils.drive import descargar_csv_drive

log_bp = Blueprint('log', __name__)

LOG_CSV_ID = "1S7IvflfqXJURLwicx_wZUqpAP4opfht5"

@log_bp.route('/log')
def log_view():
    if 'user' not in session:
        return render_template("login.html")  # o redirigir al login

    try:
        df_log = descargar_csv_drive(LOG_CSV_ID)
        registros = df_log.to_dict(orient='records')
        columnas = df_log.columns.tolist() if not df_log.empty else []
    except Exception as e:
        current_app.logger.error(f"Error al cargar el log: {e}")
        registros = []
        columnas = []

    return render_template("log.html", registros=registros, columnas=columnas)

@log_bp.route('/api/log')
def api_log():
    if 'user' not in session:
        return jsonify({"error": "No autorizado"}), 401

    try:
        df_log = descargar_csv_drive(LOG_CSV_ID)
        registros = df_log.to_dict(orient='records')
        columnas = df_log.columns.tolist() if not df_log.empty else []
        return jsonify({"registros": registros, "columnas": columnas})
    except Exception as e:
        current_app.logger.error(f"Error en API /api/log: {e}")
        return jsonify({"error": "No se pudo cargar el log"}), 500
