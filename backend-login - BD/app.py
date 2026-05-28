import os
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# Busca la línea donde pusiste CORS(app) y cámbiala por esta:
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Ruta absoluta para que apunte exactamente al archivo que creaste en el CMD
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "usuarios.db")

def buscar_usuario(username_recibido, password_recibido):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT id, username FROM usuarios WHERE username = ? AND password = ?", 
        (username_recibido, password_recibido)
    )
    usuario = cursor.fetchone()
    
    conn.close()
    return usuario

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('email')  # Tu Login.jsx envía el input username en la clave 'email'
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Faltan datos"}), 400

    usuario_encontrado = buscar_usuario(username, password)

    if usuario_encontrado:
        return jsonify({
            "message": f"¡Bienvenido de vuelta, {usuario_encontrado[1]}!",
            "user": {"id": usuario_encontrado[0], "username": usuario_encontrado[1]}
        }), 200
    else:
        return jsonify({"error": "Usuario o contraseña incorrectos"}), 401

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)