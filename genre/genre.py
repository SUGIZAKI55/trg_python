import random
from flask import Flask, redirect, url_for, render_template, request, session
from flask_session import Session
from datetime import timedelta
# from datetime import datetime

app = Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route('/genre')
def genre():
    error = None
    print(f"{genre_to_ids=}")
    return render_template('genre.html', error=error, genre_to_ids=genre_to_ids)

@app.route('/genre2', methods=['POST'])
def genre2():
    s = request.form.getlist('t') #{t:C言語}
    print(f"選択されたジャンル: {s}") #f文字
    return f"選択されたジャンル: {s}"

@app.route('/admin')
def admin():
    return "Admin Page"

topics = [
    [1, "C言語:Java:Python"],
    [2, "C言語:Ruby:C#"],
    [3, "C言語:Python"],
]
#ランダム関数を用いてC言語が２問出題となるようにする(9/8に進む）

# 各トピックのIDをジャンルごとに分類する辞書
genre_to_ids = {}

for topic in topics: #: pythonの基本でインデントの前に使われる#
    topic_id = topic[0]
    genre_list = topic[1].split(":")
    
    for genre in genre_list:
        # ジャンルに対応するIDリストを更新
        if genre in genre_to_ids:
            genre_to_ids[genre].append(topic_id) #配列に追加する場合にappendを使う
        else:
            genre_to_ids[genre] = [topic_id]

# 結果を表示
print("ジャンルごとのIDリスト:", genre_to_ids)

#答え
# ジャンルごとのIDリスト: {'C言語': [1, 2, 3], 'Java': [1], 'Python': [1, 3], 'Ruby': [2], 'C#': [2]}

if __name__ == "__main__":
    app.run(debug=True, port=8888)