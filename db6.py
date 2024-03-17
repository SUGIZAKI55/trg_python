from flask import Flask, request, jsonify, render_template_string
import sqlite3
import bcrypt

app = Flask(__name__)

def hash_password(password):
    # パスワードをハッシュ化する
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password

# SQLite3データベース接続設定
def create_db_connection():
    connection = sqlite3.connect('sugizaki.db')
    return connection

# データベースにデータを挿入する関数
def insert_user(username, password_hash):
    connection = create_db_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            query = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
            cursor.execute(query, (username, password_hash))
            connection.commit()
            cursor.close()
            connection.close()
            return "User added successfully"
        except sqlite3.Error as e:
            return f"The error '{e}' occurred"
    else:
        return "Failed to create database connection"

# ユーザーを追加するルート
@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.form['username']
    password = request.form['password_hash']
    password_hash = hash_password(password)
    result = insert_user(username, password_hash)
    return jsonify({'message': result})

# フォームを表示するためのルート
@app.route('/')
def index():
    # HTMLフォーム
    html_form = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ユーザー登録フォーム</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        <style>
            body {
                background-color: #f8f9fa;
                margin-top: 50px;
            }
            .container {
                background-color: #fff;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0px 0px 10px 0px rgba(0,0,0,0.1);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2 class="mb-4">ユーザー登録フォーム</h2>
            <form action="/add_user" method="post">
                <div class="form-group">
                    <label for="username">ユーザー名:</label>
                    <input type="text" class="form-control" id="username" name="username">
                </div>
                <div class="form-group">
                    <label for="password_hash">パスワード:</label>
                    <input type="password" class="form-control" id="password_hash" name="password_hash">
                </div>
                <button type="submit" class="btn btn-primary">登録</button>
            </form>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html_form)

if __name__ == '__main__':
    app.run(debug=True)
