import json
from werkzeug.security import generate_password_hash

# Usuario, contraseña y carpeta de Drive que quieres crear
usuario = input("Nombre de usuario: ")
contrasena = input("Contraseña: ")
carpeta_drive = input("ID de la carpeta de Google Drive para este usuario: ")

# Hashear la contraseña
hashed = generate_password_hash(contrasena)

# Cargar archivo existente (o crear uno vacío)
try:
    with open("users.json", "r") as f:
        users = json.load(f)
except FileNotFoundError:
    users = {}

# Añadir nuevo usuario con carpeta asociada
users[usuario] = {
    "password": hashed,
    "carpeta_drive": carpeta_drive
}

# Guardar el archivo actualizado
with open("users.json", "w") as f:
    json.dump(users, f, indent=4)

print(f"Usuario '{usuario}' creado correctamente con carpeta '{carpeta_drive}'.")

