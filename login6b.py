import bcrypt
from flask import Flask, redirect, url_for, render_template, request, session
from flask_session import Session
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# SQLite3データベース接続設定
def create_db_connection():
    connection = sqlite3.connect('sugizaki.db')
    return connection

# ユーザーの認証を行う関数
def authenticate_user(username, password):
    connection = create_db_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            query = "SELECT password_hash FROM users WHERE username = ?"
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            if result:
                hashed_password = result[0]
                if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                    return True
        except sqlite3.Error as e:
            print(f"The error '{e}' occurred")
        finally:
            cursor.close()
            connection.close()
    return False

@app.route('/')
def login_form():
    # GETリクエストの処理: ログインフォームを表示
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    # POSTリクエストの処理: ログインフォームからのデータを処理
    username = request.form['username']
    password = request.form['password']

    if authenticate_user(username, password):
        # ログイン成功
        session['username'] = username
        return redirect(url_for('loginok'))  # ログイン後のページにリダイレクト
    else:
        return render_template("error.html")

@app.route('/loginok', methods=['GET'])
def loginok():
    return render_template("loginok.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        connection = create_db_connection()
        if connection is not None:
            try:
                cursor = connection.cursor()
                query = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
                cursor.execute(query, (username, hashed_password))
                connection.commit()
                cursor.close()
                connection.close()
                return redirect(url_for('login_form'))  # 登録後にログイン画面にリダイレクト
            except sqlite3.Error as e:
                print(f"The error '{e}' occurred")
                return render_template("error.html")
    return render_template("signup.html")

if __name__ == "__main__":
    app.run(debug=True, port=8888)
