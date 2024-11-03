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
    return redirect(url_for('admin'))

@app.route('/admin')
def admin():
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

# @app.route('/farstquestion')


@app.route('/question',methods=['GET'])
def question():
    if 'username' not in session:
        return redirect(url_for('login'))
    else:
        Q_no = session["Q_no"]
        qmap = session["qmap"]
        print(f"@126 {Q_no=} {qmap=}")
        qmaped_Q_no = qmap[Q_no]
        qmaped_Q_no = int(qmaped_Q_no) #文字を数字変換
        # number = session["number"]
        # genre_no = session["genre_no"]
        # print("qmaped_Q_no=",qmaped_Q_no)
        # print("quiz_questions===",quiz_questions)
        quiz_item = quiz_questions[qmaped_Q_no] #quiz_questionsから1つ取り出したもの
        answer_choices = quiz_item[3].split(":") #回答群
        if len(answer_choices) < 4:
            max_choices = len(answer_choices)
        else:
            max_choices = 4    
        selected_choices = random.sample(answer_choices, max_choices) #selected_choicesは出題の回答群で要素の数が4つ以下 、配列
        # print(f"{selected_choices=}")
        session["selected_choices"] = selected_choices
        correct_answers_temp = set(quiz_item[4].split(":")) #正解群
        correct_choices = set(selected_choices) & correct_answers_temp #setで配列を集合形に変換&
        session["correct_ans"] = correct_choices

        start_datetime = datetime.now()
        formatted_date_string = start_datetime.strftime('%Y-%m-%d %H:%M:%S')
        session["start_datetime"] = formatted_date_string

        genre_name = session["genre_name"]
        # genre_name = request.form.getlist('category')  # 選択されたジャンルを取得
        # print(f"選択されたジャンル: {genre_name}")
        # print(f"ジャンル表示: {genre_to_ids=}")

        return render_template('question.html', question=quiz_item[2], choices=selected_choices,genre_name=genre_name)

@app.route('/answer', methods=['GET'])
def check_answer():
    selected_choices = session["selected_choices"] #問題にセッションを持たせる
    correct_ans = session.get("correct_ans", set())
    list_correct_ans = list(correct_ans) #集合型を配列にした
    print(f"{list_correct_ans=}")
    answer_feedback ={}
    for sentaku in selected_choices:
        if sentaku in list_correct_ans:
            answer_feedback[sentaku] = "○"
        else:
            answer_feedback[sentaku] = "×"
    print(answer_feedback)

    user_choice = request.args.getlist('choice[]')
    end_datetime = datetime.now()
    date_string = session["start_datetime"]
    start_datetime = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
    elapsed_time = end_datetime - start_datetime
    elapsed_time_str = str(elapsed_time)
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
