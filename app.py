import random
from flask import Flask, redirect, url_for, render_template, request, session
from flask_session import Session
import sqlite3
import bcrypt
from datetime import timedelta
from createquiz import app
from datetime import datetime

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

genre_to_ids = {} #グローバル宣言をした

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
            selected_choices = cursor.fetchone()
            if selected_choices:
                hashed_password = selected_choices[0]
                if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                    return True
        except sqlite3.Error as e:
            print(f"The error '{e}' occurred")
        finally:
            cursor.close()
            connection.close()
    return False

with open('quiz_questions.txt', 'r', encoding='utf-8') as file:
    content = file.read().strip()
questions = content.split('\n\n')
quiz_questions = []
for question in questions:
    parts = question.split('\n')
    if len(parts) == 6:
        quiz_questions.append(parts)
# print(f"@50=={quiz_questions=}")
for topic in quiz_questions: #: pythonの基本でインデントの前に使われる#
    topic_id = topic[0]
    genre_list = topic[1].split(":")
    
    for genre in genre_list:
        # ジャンルに対応するIDリストを更新
        if genre in genre_to_ids:
            genre_to_ids[genre].append(topic_id) #配列に追加する場合にappendを使う
        else:
            genre_to_ids[genre] = [topic_id]
# print(f"@61=={genre_to_ids=}")

@app.route('/')
def login_form():
    error = request.args.get('error')
    return render_template('login.html', error=error)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if authenticate_user(username, password):
        session['username'] = username
        return redirect(url_for('loginok'))
    else:
        return render_template('error.html')  # ログイン失敗時にerror.htmlを表示

@app.route('/loginok')
def loginok():
    session["Q_no"] = 0 #セッションが辞書型{"Q_no":0} ※サーバー側にある
    if 'username' in session:
        username = session['username']  # セッションからユーザー名を取得
        return render_template('admin.html', username=username)
    else:
        return redirect(url_for('login_form'))


@app.route('/admin')
def admin():
    if 'username' in session:  # セッションからユーザー名を取得
        username = session['username']
        return render_template('admin.html', username=username)
    else:
        return redirect(url_for('login_form'))  # ログイン画面へリダイレクト
    return render_template('admin.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.clear()
    return redirect(url_for('login_form'))

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
                return redirect(url_for('login_form'))
            except sqlite3.Error as e:
                print(f"The error '{e}' occurred")
                return render_template('error.html')
    return render_template("signup.html")

@app.route('/question', methods=['GET'])
def question():
    # ユーザーがログインしていない場合はログインページにリダイレクト
    if 'username' not in session:
        return redirect(url_for('login'))
    else:
        # 現在の問題番号をセッションから取得
        Q_no = session["Q_no"]

        # 現在のジャンルに対応する問題のマッピングをセッションから取得
        qmap = session["qmap"]

        # 現在の問題番号から対応する問題IDを取得
        qmaped_Q_no = qmap[Q_no]
        qmaped_Q_no = int(qmaped_Q_no)  # 文字列を整数に変換

        # 対応する問題を `quiz_questions` から取り出す
        quiz_item = quiz_questions[qmaped_Q_no]  # `quiz_questions` から1つの問題を取得

        # 回答群を取得し、':'で分割してリスト化
        answer_choices = quiz_item[3].split(":")

        # 回答群の数が4未満の場合はその数まで、4以上の場合は最大4つを選択肢としてランダム抽出
        if len(answer_choices) < 4:
            max_choices = len(answer_choices)
        else:
            max_choices = 4
        selected_choices = random.sample(answer_choices, max_choices)  # ランダムで選択肢を抽出

        # 選択肢をセッションに保存
        session["selected_choices"] = selected_choices

        # 正解群をセットに変換（重複を排除）
        correct_answers_temp = set(quiz_item[4].split(":"))  # 正解群を取得
        correct_choices = set(selected_choices) & correct_answers_temp  # 選択肢と正解群の共通部分を取得
        session["correct_ans"] = correct_choices  # 正解をセッションに保存

        # 問題が開始された日時をセッションに保存
        start_datetime = datetime.now()
        formatted_date_string = start_datetime.strftime('%Y-%m-%d %H:%M:%S')  # 日時をフォーマット
        session["start_datetime"] = formatted_date_string

        # 現在選択されたジャンル名をセッションから取得
        genre_name = session["genre_name"]

        # 質問テンプレートをレンダリングし、必要なデータを渡す
        return render_template(
            'question.html',
            question=quiz_item[2],  # 問題文
            choices=selected_choices,  # 選択肢
            genre_name=genre_name  # ジャンル名
        )

@app.route('/answer', methods=['GET'])
def check_answer():
    # 選択された回答をセッションから取得
    selected_choices = session["selected_choices"]  # 問題の選択肢がセッションに保存されている
    
    # セッションから正解を取得。正解が無い場合、デフォルトで空の集合（set）を返す
    correct_ans = session.get("correct_ans", set())
    
    # 正解をリストに変換（後の処理でリスト操作を行うため）
    list_correct_ans = list(correct_ans)
    print(f"{list_correct_ans=}")  # デバッグ用出力
    
    # 選択肢ごとの正誤を保持する辞書
    answer_feedback = {}
    for sentaku in selected_choices:  # ユーザーに表示された選択肢を1つずつチェック
        if sentaku in list_correct_ans:  # 選択肢が正解に含まれているかどうかを確認
            answer_feedback[sentaku] = "○"  # 正解の場合
        else:
            answer_feedback[sentaku] = "×"  # 不正解の場合
    print(answer_feedback)  # 選択肢ごとの正誤結果をデバッグ出力

    # ユーザーが選択した回答をリクエストパラメータから取得
    user_choice = request.args.getlist('choice[]')  # フォームから送られてきたデータをリスト形式で取得

    # 現在の日時を取得して、回答時間を計算
    end_datetime = datetime.now()  # 回答が終了した時刻
    date_string = session["start_datetime"]  # セッションに保存されている開始時刻
    start_datetime = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')  # 開始時刻を文字列から日時オブジェクトに変換
    elapsed_time = end_datetime - start_datetime  # 経過時間を計算
    elapsed_time_str = str(elapsed_time)  # 経過時間を文字列としてフォーマット

    # ユーザーが選択した回答を集合（set）として変換（重複を排除するため）
    user_set = set(user_choice)

    if user_set == correct_ans:
        answer = "正解"
    else:
        answer = f"不正解。正しい答えは: {', '.join(correct_ans)}"

    Q = session["Q_no"] #1問目が終わったら大元のインデックスに+1される
    Q += 1
    session["Q_no"] = Q

    user_choice_str = ', '.join(user_choice)
    correct_ans_str = ', '.join(correct_ans)

    return render_template('kekka.html', answer=answer, et=elapsed_time_str, Q_no=Q, user_choice=user_choice_str, correct_ans=correct_ans_str ,answer_feedback=answer_feedback)

@app.route('/genre') #@~デコレーター、関数を飾るもの
def genre():
    error = None
    # print(f"{genre_to_ids=}")
    return render_template('genre.html', error=error, genre_to_ids=genre_to_ids)

@app.route('/firstquestion', methods=['POST'])
def firstquestion():
    genre_name = request.form.getlist('category')  # 選択されたジャンルを取得
    # print(f"選択されたジャンル: {genre_name}")
    # print(f"ジャンル表示: {genre_to_ids=}")
    session["genre_name"]=genre_name
    
    genre_no = genre_to_ids[genre_name[0]]  # 選択されたジャンルに対応する問題のIDリストを取得
    # print(f"選択したジャンルの表示: {genre_no=}")
    session["genre_no"]=genre_no
    
    number = int(request.form['nanko'])  # 取り出す問題数を取得
    # print(f"number: {number=}")
    session["number"]=number
    
    # qmapは、ジャンルに対応する問題IDをランダムに抽出したリスト
    qmap = random.sample(genre_no, number)
    # print(f"qmap: {qmap=}")  # ランダムで抽出された問題のIDリスト
    session["qmap"]=qmap

    Q_no = 0
    session["Q_no"] = Q_no

    return render_template('first.html')

@app.route('/admin2')
def admin2():
    return "Admin Page"

if __name__ == "__main__":
    app.run(debug=True, port=8888)
