# crear_usuario.py
import json
from werkzeug.security import generate_password_hash

# Usuario y contraseña que quieres crear
usuario = input("Nombre de usuario: ")
contrasena = input("Contraseña: ")

# Hashear la contraseña
hashed = generate_password_hash(contrasena)

# Cargar archivo existente (o crear uno vacío)
try:
    with open("users.json", "r") as f:
        users = json.load(f)
except FileNotFoundError:
    users = {}

# Añadir nuevo usuario
users[usuario] = {"password": hashed}

# Guardar el archivo actualizado
with open("users.json", "w") as f:
    json.dump(users, f, indent=4)

print(f"Usuario '{usuario}' creado correctamente.")

