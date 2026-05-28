import os
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# Apertura total de CORS para que Vercel pueda entrar sin problemas
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Ruta absoluta inteligente
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "usuarios.db")

def inicializar_base_de_datos():
    """Crea la base de datos, la tabla y el admin automáticamente si no existen."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Creamos la tabla si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    
    # Insertamos al admin de la UNFV si la tabla está vacía
    cursor.execute("SELECT * FROM usuarios WHERE username = 'admin'")
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO usuarios (username, password) VALUES (?, ?)", 
            ('admin', 'password123')
        )
        print("🟢 BASE DE DATOS LOCAL LISTA: Usuario 'admin' y tabla creados.")
    
    conn.commit()
    conn.close()

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('email')  
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Faltan datos"}), 400

    # Buscar usuario directamente
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM usuarios WHERE username = ? AND password = ?", (username, password))
    usuario_encontrado = cursor.fetchone()
    conn.close()

    if usuario_encontrado:
        return jsonify({
            "message": f"¡Bienvenido de vuelta, {usuario_encontrado[1]}!",
            "user": {"id": usuario_encontrado[0], "username": usuario_encontrado[1]}
        }), 200
    else:
        return jsonify({"error": "Usuario o contraseña incorrectos"}), 401

if __name__ == '__main__':
    # EJECUTAR SI O SI AL ARRANCAR
    inicializar_base_de_datos()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)