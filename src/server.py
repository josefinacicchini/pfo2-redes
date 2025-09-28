import os
import sys
import sqlite3
from flask import Flask, request, jsonify, g, session, render_template_string
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'mi_clave_secreta_123'  #para manejar sesiones

# --- Database setup ---
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    # Table for users
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

init_db()

# --- Routes ---
@app.route('/registro', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"mensaje": "Faltan datos"}), 400

    hashed_password = generate_password_hash(password)

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({"mensaje": "Usuario ya existe"}), 400
    finally:
        conn.close()

    return jsonify({"mensaje": "Usuario registrado con exito"}), 201

#----login route----
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT id, password FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()

    if user and check_password_hash(user[1], password):
        session['user_id'] = user[0]  # guarda el id del usuario en sesión
        return jsonify({"mensaje": "Inicio de sesion exitoso"}), 200
    else:
        return jsonify({"mensaje": "Credenciales invalidas"}), 401

#----tareas route----
@app.route('/tareas', methods=['GET'])
def tareas():
    if 'user_id' not in session:  # prote el endpoint
        return jsonify({"mensaje": "Acceso denegado, primero haz login"}), 401

    html = """
    <h1>Bienvenido a la gestión de tareas</h1>
    <p></p>
    """
    return render_template_string(html)

#----logout route----
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None) 
    return jsonify({"mensaje": "Sesión cerrada"}), 200



if __name__ == '__main__':
    app.run(debug=True)


