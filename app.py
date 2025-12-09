import sqlite3
from flask import Flask, request, render_template, redirect, session

app = Flask(__name__)
app.secret_key = "vulnerable"

# ---------------------------
# INIT DB
# ---------------------------
def init_db():
    conn = sqlite3.connect("notes.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ---------------------------
# Уязвимая регистрация
# ---------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Уязвимый SQL
        query = f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')"

        try:
            conn = sqlite3.connect("notes.db")
            c = conn.cursor()
            c.execute(query)
            conn.commit()
        except Exception as e:
            return f"SQL Error: {e}"

        return redirect("/login")

    return render_template("register.html")












# ---------------------------
# Уязвимый логин
# ---------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Уязвимый SQL
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"

        print("EXECUTED QUERY:", query)

        conn = sqlite3.connect("notes.db")
        c = conn.cursor()
        c.execute(query)
        user = c.fetchone()

        if user:
            session["user"] = user[1]
            return f"Успешный вход! Вы вошли как: {user[1]}"

        return "Неверные данные!"

    return render_template("login.html")







@app.route("/")
def index():
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)
