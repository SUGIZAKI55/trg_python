from flask import Flask, request, jsonify, render_template_string
import mysql.connector
import bcrypt
from mysql.connector import Error

app = Flask(__name__)

# データベース接続設定
def create_db_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',           # データベースサーバーのアドレス
            user='root',                # データベースのユーザー名
            password='',                # ユーザーのパスワード
            database='sugizaki'         # 接続するデータベース名
        )
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

# データベースにデータを挿入する関数
def insert_user(username, password_hash):
    connection = create_db_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            query = "INSERT INTO users (username, password_hash) VALUES (%s, %s)"
            cursor.execute(query, (username, password_hash))
            connection.commit()
            cursor.close()
            connection.close()
            return "User added successfully"
        except Error as e:
            return f"The error '{e}' occurred"
    else:
        return "Failed to create database connection"

# ユーザーを追加するルート
@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.form['username']
    password_hash = request.form['password_hash']
    result = insert_user(username, password_hash)
    return jsonify({'message': result})

# フォームを表示するためのルート
@app.route('/')
def index():
    # HTMLフォーム
    html_form = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Add User</title>
    </head>
    <body>
        <h2>Add User</h2>
        <form action="/add_user" method="post">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username"><br><br>
            <label for="password_hash">Password Hash:</label>
            <input type="text" id="password_hash" name="password_hash"><br><br>
            <input type="submit" value="Submit">
        </form>
    </body>
    </html>
    '''
    return render_template_string(html_form)

if __name__ == '__main__':
    app.run(debug=True)



# ユーザーから受け取ったパスワード
password = "user_password_here"

# パスワードをバイト文字列に変換
password_bytes = password.encode('utf-8')

# パスワードのハッシュを生成（ソルトは自動的に生成される）
hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

# ハッシュ化されたパスワードを表示（データベースに保存する値）
print(hashed_password)

# ハッシュ化されたパスワードをバイト列から文字列に変換して保存や比較に使いやすくする
hashed_password_str = hashed_password.decode('utf-8')
print(hashed_password_str)
