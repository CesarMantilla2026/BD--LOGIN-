import os
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# 🔥 ESTO SOLUCIONA EL ERROR 500 EN RENDER COMPLETAMENTE:
if os.environ.get('RENDER'):
    # En la nube de Render guardamos en /tmp, la única carpeta con permisos de escritura libres
    DATABASE = "/tmp/usuarios.db"
else:
    # En tu computadora local se guarda normal en tu carpeta
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATABASE = os.path.join(BASE_DIR, "usuarios.db")

def inicializar_base_de_datos():
    """Crea la base de datos, la tabla y el admin automáticamente."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # 1. Creamos la tabla con la columna 'username'
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    
    # 2. Verificamos e insertamos al admin con las columnas correctas
    cursor.execute("SELECT * FROM usuarios WHERE username = 'admin'")
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO usuarios (username, password) VALUES (?, ?)", 
            ('admin', 'password123')
        )
        print("🟢 ¡BASE DE DATOS CREADA DESDE CERO CON ÉXITO!")
    
    conn.commit()
    conn.close()

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    
    username = data.get('username')  
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Faltan datos en la petición"}), 400

    # 🌟 HACEMOS LA BÚSQUEDA DIRECTAMENTE AQUÍ (Sin llamar a funciones externas inexistentes)
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM usuarios WHERE username = ? AND password = ?", (username, password))
    usuario_encontrado = cursor.fetchone()
    conn.close()

    # Validamos el resultado
    if usuario_encontrado:
        return jsonify({
            "message": f"¡Bienvenido de vuelta, {usuario_encontrado[1]}!",
            "user": {"id": usuario_encontrado[0], "username": usuario_encontrado[1]}
        }), 200
    else:
        return jsonify({"error": "Usuario o contraseña incorrectos"}), 401

# Busca el final de tu app.py y déjalo exactamente así:
if __name__ == '__main__':
    inicializar_base_de_datos()  # <-- Esto creará la tabla y el admin en /tmp automáticamente
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)