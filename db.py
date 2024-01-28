from flask import Flask
import mysql.connector

app = Flask(__name__)

# データベース設定
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'sugizaki'
}

@app.route('/')
def index():
    # データベースに接続
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()

    # クエリの実行
    cursor.execute("SELECT * FROM users")

    # 結果の取得
    users = cursor.fetchall()

    # 接続の終了
    cursor.close()
    cnx.close()

    # 結果を表示（例として）
    return str(users)

if __name__ == '__main__':
    app.run(debug=True)