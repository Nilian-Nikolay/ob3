import sqlite3
from flask import Flask, request, render_template, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")  # обязательная переменная окружения

# ----------------------------------------
# Подключение к БД
# ----------------------------------------
def get_db():
    conn = sqlite3.connect("notes.db")
    conn.row_factory = sqlite3.Row
    return conn

# ----------------------------------------
# Инициализация базы
# ----------------------------------------
def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()

# ----------------------------------------
# REGISTER (GET)
# ----------------------------------------
@app.route('/register', methods=['GET'])
def register_form():
    return render_template("register.html")

# ----------------------------------------
# REGISTER (POST)
# ----------------------------------------
@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()

    if not username or not password:
        return "Введите логин и пароль!"

    hashed = generate_password_hash(password)

    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        return "Такой пользователь уже существует!"
    finally:
        conn.close()

    return redirect("/login")

# ----------------------------------------
# LOGIN (GET)
# ----------------------------------------
@app.route('/login', methods=['GET'])
def login_form():
    return render_template("login.html")

# ----------------------------------------
# LOGIN (POST)
# ----------------------------------------
@app.route('/login', methods=['POST'])
def login_handler():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username, password FROM users WHERE username = ?", 
        (username,)
    )
    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user["password"], password):
        session['user_id'] = user["id"]
        session['username'] = user["username"]
        return redirect("/profile")
    else:
        return "Неверные данные!"

# ----------------------------------------
# PROFILE
# ----------------------------------------
@app.route("/profile")
def profile():
    if 'user_id' not in session:
        return redirect("/login")
    return f"Добро пожаловать, {session['username']}!"

# ----------------------------------------
# LOGOUT
# ----------------------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ----------------------------------------
# DEFAULT route
# ----------------------------------------
@app.route("/")
def index():
    return redirect("/login")

if __name__ == "__main__":
    host = os.getenv("FLASK_HOST", "127.0.0.1")
    port = int(os.getenv("FLASK_PORT", "5000"))
    app.run(host=host, port=port, debug=False)
