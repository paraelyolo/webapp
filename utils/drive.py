# utils/drive.py

import pandas as pd
import requests
from io import StringIO

def descargar_csv_drive(file_id):
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("No se pudo descargar el archivo.")
    return pd.read_csv(StringIO(response.text))

