from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# データベース接続設定
def create_db_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',           # データベースサーバーのアドレス
            user='root',       # データベースのユーザー名
            password='',   # ユーザーのパスワード
            database='sugizaki'    # 接続するデータベース名
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
@app.route('/add_user', methods=['GET'])
def add_user():
    data = request.get_json()
    username = data['username']
    password_hash = data['password_hash']
    result = insert_user(username, password_hash)
    return jsonify({'message': result})

if __name__ == '__main__':
    app.run(debug=True)
