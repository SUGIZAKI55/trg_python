import random
import json
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

genre_to_ids = {}  # ジャンルとIDの対応を保持

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
for topic in quiz_questions:
    topic_id = topic[0]
    genre_list = topic[1].split(":")
    for genre in genre_list:
        if genre in genre_to_ids:
            genre_to_ids[genre].append(topic_id)
        else:
            genre_to_ids[genre] = [topic_id]

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
        return render_template('error.html')

@app.route('/loginok')
def loginok():
    session["Q_no"] = 0  # 現在の問題番号を初期化
    if 'username' in session:
        username = session['username']
        return render_template('admin.html', username=username)
    else:
        return redirect(url_for('login_form'))

@app.route('/admin')
def admin():
    if 'username' in session:
        username = session['username']
        return render_template('admin.html', username=username)
    else:
        return redirect(url_for('login_form'))

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
    if 'username' not in session:
        return redirect(url_for('login'))
    else:
        Q_no = session["Q_no"]
        qmap = session["qmap"]
        qmaped_Q_no = qmap[Q_no]
        qmaped_Q_no = int(qmaped_Q_no)
        quiz_item = quiz_questions[qmaped_Q_no]
        
        # 問題IDを正確に保存
        question_id = quiz_item[0]
        session["current_question_id"] = question_id

        answer_choices = quiz_item[3].split(":")

        if len(answer_choices) < 4:
            max_choices = len(answer_choices)
        else:
            max_choices = 4
        selected_choices = random.sample(answer_choices, max_choices)

        session["selected_choices"] = selected_choices
        correct_answers_temp = set(quiz_item[4].split(":"))
        correct_choices = set(selected_choices) & correct_answers_temp
        session["correct_ans"] = correct_choices

        start_datetime = datetime.now()
        formatted_date_string = start_datetime.strftime('%Y-%m-%d %H:%M:%S')
        session["start_datetime"] = formatted_date_string

        genre_name = session["genre_name"]
        return render_template('question.html', question=quiz_item[2], choices=selected_choices, genre_name=genre_name)

def log_w(data):
    with open('seiseki.ndjson', 'a', encoding='utf-8') as file:
        json_string = json.dumps(data, ensure_ascii=False)
        file.write(json_string + '\n')
        print("データを改行区切りJSON形式で保存しました。")

@app.route('/answer', methods=['GET'])
def check_answer():
    selected_choices = session["selected_choices"]
    correct_ans = session.get("correct_ans", set())
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

    Q = session["Q_no"]
    Q += 1
    session["Q_no"] = Q

    user_choice_str = ', '.join(user_choice)
    correct_ans_str = ', '.join(correct_ans)

    data = {
        "date": datetime.now().strftime('%Y-%m-%d'),
        "name": session.get("username", "不明"),
        # "genre": ', '.join(session["genre_name"]),
        "genre": session["genre_name"][0],
        "qmap": session["qmap"],
        "question_id": session["current_question_id"],
        "start_time": start_datetime.strftime('%H:%M:%S'),
        "end_time": end_datetime.strftime('%H:%M:%S'),
        "elapsed_time": elapsed_time_str,
        "user_choice": user_choice,
        "correct_answers": list(correct_ans),
        "result": answer
    }
    log_w(data)
    print(f"記録されるデータ: {data}")
    return render_template('kekka.html', answer=answer, et=elapsed_time_str, Q_no=Q, user_choice=user_choice_str, correct_ans=correct_ans_str, answer_feedback={c: ("○" if c in correct_ans else "×") for c in selected_choices})

@app.route('/genre')
def genre():
    error = None
    return render_template('genre.html', error=error, genre_to_ids=genre_to_ids)

@app.route('/firstquestion', methods=['POST'])
def firstquestion():
    genre_name = request.form.getlist('category')
    session["genre_name"] = genre_name
    genre_no = genre_to_ids[genre_name[0]]
    session["genre_no"] = genre_no
    number = int(request.form['nanko'])
    session["number"] = number
    qmap = random.sample(genre_no, number)
    session["qmap"] = qmap
    Q_no = 0
    session["Q_no"] = Q_no
    return render_template('first.html')

@app.route('/view', methods=['GET'])
def view():
    # ファイルを読み込み
    filename = "seiseki.ndjson"

    # 名前とジャンルごとに正解数と問題数を記録する辞書
    result_data = {}
    username = session['username']

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                # 各行を辞書型に変換
                record = json.loads(line.strip())
                name = record["name"]
                # genres = record["genre"].strip().split(":")  # 修正1: 複数ジャンルを分割してリストにする
                # genre = record["genre"].strip() #2/9
                genres = record["genre"].strip().split(":") if "genre" in record and record["genre"] else ["不明"]
                result = record["result"]
                question_id = record.get("question_id", "不明")

                for genre in genres:  # 修正2: 各ジャンルごとにデータを処理
                    # 名前が辞書に存在しなければ初期化
                    if name not in result_data:
                        result_data[name] = {}

                    # ジャンルが辞書に存在しなければ初期化
                    if genre not in result_data[name]:
                        result_data[name][genre] = {"correct": 0, "total": 0, "error": []}

                    # 総問題数を1増加
                    result_data[name][genre]["total"] += 1

                    # 正確に "正解" と一致する場合のみ正解数を増加
                    if result.strip() == "正解":
                        result_data[name][genre]["correct"] += 1
                    else:
                        result_data[name][genre]["error"].append(question_id)

        # 名前とジャンル別に正答率を計算して出力
        for name, genres in result_data.items():
            print(f"名前: {name}")
            for genre, data in genres.items():
                total = data["total"]
                correct = data["correct"]
                error = data["error"]

                # 正答率の計算
                if total > 0:
                    accuracy = (correct / total) * 100
                else:
                    accuracy = 0

                print(f"  ジャンル: {genre}, 正答率: {accuracy:.2f}% ({correct}/{total}), 間違ったID: {', '.join(error) if error else 'なし'}")

        ans = result_data[username]

    except FileNotFoundError:
        print(f"ファイル '{filename}' が見つかりません。")
    except json.JSONDecodeError:
        print("JSON データの解析中にエラーが発生しました。")

    return render_template('view.html', ans=ans)

@app.route('/retry/<question_id>', methods=['GET'])
def retry_question(question_id):
    # 問題IDに基づいて該当する問題を探す
    quiz_item = next((q for q in quiz_questions if q[0] == question_id), None)

    if quiz_item is None:
        return "問題が見つかりませんでした。", 404

    # 問題データをセッションに保存して再出題
    session["current_question_id"] = question_id
    answer_choices = quiz_item[3].split(":")
    
    if len(answer_choices) < 4:
        max_choices = len(answer_choices)
    else:
        max_choices = 4

    selected_choices = random.sample(answer_choices, max_choices)
    session["selected_choices"] = selected_choices
    correct_answers_temp = set(quiz_item[4].split(":"))
    correct_choices = set(selected_choices) & correct_answers_temp
    session["correct_ans"] = correct_choices

    genre_name = quiz_item[1].split(":")[0]  #2/9追加
    session["genre_name"] = [genre_name]

    start_datetime = datetime.now()
    formatted_date_string = start_datetime.strftime('%Y-%m-%d %H:%M:%S')
    session["start_datetime"] = formatted_date_string
    session["genre_name"] = [quiz_item[1]]  # ジャンルを設定

    return render_template('question.html', question=quiz_item[2], choices=selected_choices, genre_name=quiz_item[1])

if __name__ == "__main__":
    app.run(debug=True, port=8888)
