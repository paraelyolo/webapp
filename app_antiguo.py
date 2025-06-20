from flask import Flask, render_template, redirect, session
from utils.drive import descargar_csv_drive

app = Flask(__name__)
app.secret_key = 'superclave'

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')

    archivos = {
        "operador": "1uIgigavolkY6xdWKw1DCEGmfsBD_wzn6",
        "horas": "152IQbofX1hAKODLmOU8HJErDHW142hNH",
        "piezas": "1EkZoRWAlvOMm9ED4cQJgmhAA_VAwOPi4",
        "perfil": "1Q6mnuyx80XRIohbxVu4cgimRyZP3J85A"
    }

    datos = {}
    for clave, file_id in archivos.items():
        try:
            df = descargar_csv_drive(file_id)
            datos[clave] = str(df.values[0][0])
        except Exception as e:
            datos[clave] = f"Error: {e}"

    return render_template('dashboard.html', datos=datos)

# 👇 Aquí pegas el nuevo bloque para el log
@app.route('/log/<machine>')
def log(machine):
    if 'user' not in session:
        return redirect('/')
    
    logs_drive_ids = {
        "maquina1": "1HyZb9Mxezy2hcfUd1-ZdOMWo-QjzUXtZ"
    }

    file_id = logs_drive_ids.get(machine)
    if not file_id:
        return f"No se encontró log para la máquina {machine}", 404

    try:
        df = descargar_csv_drive(file_id)
        table_html = df.to_html(classes='csv-table', index=False)
    except Exception as e:
        table_html = f"<p>Error al cargar CSV: {e}</p>"

    return render_template('log.html', machine=machine, table_html=table_html)

