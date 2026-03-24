from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


# 🔴 Vulnerable Login
@app.route('/vulnerable_login', methods=['POST'])
def vulnerable_login():
    username = request.form['username']
    password = request.form['password']

    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        cursor.execute(query)

        user = cursor.fetchone()

        if user:
            return render_template("result.html", msg="HACKED 😈", img="evil.png")
        else:
            return render_template("result.html", msg="FAILED ❌", img="fail.png")

    except:
        # 👇 THIS HANDLES ERROR
        return render_template("result.html", msg="SQL ERROR 😈", img="evil.png")

# 🟢 Secure Login
@app.route('/secure_login', methods=['POST'])
def secure_login():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    query = "SELECT * FROM users WHERE username=? AND password=?"
    cursor.execute(query, (username, password))

    user = cursor.fetchone()

    if user:
        return render_template("result.html", msg="SUCCESS ✅", img="success.png")
    else:
        return render_template("result.html", msg="FAILED ❌", img="fail.png")


if __name__ == '__main__':
    app.run(debug=True)