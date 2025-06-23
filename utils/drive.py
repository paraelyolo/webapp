import requests
import pandas as pd
from io import StringIO

def descargar_csv_drive(file_id, con_encabezado=True):
    """
    Descarga un CSV desde Google Drive y lo convierte a un DataFrame de pandas.
    """
    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()

    response = session.get(URL, params={'id': file_id}, stream=True)
    token = _get_confirm_token(response)

    if token:
        params = {'id': file_id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    content = response.content.decode('utf-8')
    print("Contenido CSV descargado:")
    print(content[:500])  # muestra las primeras 500 letras

    if con_encabezado:
        return pd.read_csv(StringIO(content))
    else:
        return pd.read_csv(StringIO(content), header=None)

def _get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None
