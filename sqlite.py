import sqlite3

connection = sqlite3.connect('/Users/sugizaki/mydatabase.db')

# クエリを実行するためのカーソルを作成
cursor = connection.cursor()

# クエリを実行
cursor.execute("SELECT * FROM users")

# 結果を取得
results = cursor.fetchall()

# 結果を表示
for row in results:
    print(row)

connection.close()
