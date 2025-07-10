from flask import Flask, request, render_template_string
import sqlite3
import hashlib
import os

# Crear base de datos y tabla si no existen
DB_NAME = "usuarios.db"

def crear_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            nombre TEXT PRIMARY KEY,
            password_hash TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Función para agregar usuarios
def agregar_usuario(nombre, contraseña):
    hash_pass = hashlib.sha256(contraseña.encode()).hexdigest()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (nombre, password_hash) VALUES (?, ?)", (nombre, hash_pass))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Ya existe el usuario
    conn.close()

# Validar usuario
def validar_usuario(nombre, contraseña):
    hash_pass = hashlib.sha256(contraseña.encode()).hexdigest()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE nombre = ? AND password_hash = ?", (nombre, hash_pass))
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None

# HTML simple
html = '''
<!DOCTYPE html>
<html>
    <body>
        <h2>Login de Usuarios</h2>
        <form method="POST">
            Usuario: <input name="usuario"><br>
            Contraseña: <input type="password" name="contraseña"><br>
            <input type="submit" value="Iniciar sesión">
        </form>
        <p>{{ mensaje }}</p>
    </body>
</html>
'''

# Flask App
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def login():
    mensaje = ""
    if request.method == "POST":
        usuario = request.form["usuario"]
        contraseña = request.form["contraseña"]
        if validar_usuario(usuario, contraseña):
            mensaje = "✅ Acceso concedido"
        else:
            mensaje = "❌ Acceso denegado"
    return render_template_string(html, mensaje=mensaje)

if __name__ == "__main__":
    crear_db()
    
    # Agrega usuarios por única vez (nombres de integrantes)
    integrantes = {
        "Renatto": "clave1"
           }

    for nombre, clave in integrantes.items():
        agregar_usuario(nombre, clave)

    app.run(host="0.0.0.0", port=5800)
