from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 問題をファイルから読み込む関数
def load_questions():
    try:
        with open('quiz_questions.txt', 'r', encoding='utf-8') as file:
            lines = file.read().split('\n\n') #ファイルを読んで、2改行があったら分ける
        # print(f"@=9====={lines=}") #デバッグ出力
        questions = [] 
        for line in lines:
            # print(f"@=11====={line=}") #デバッグ出力
            parts = line.split('\n')
            # print("@=15",len(parts))
            if len(parts) == 6:
                questions.append({'Q_no':parts[0],'genre':parts[1],'title': parts[2], 'choices': parts[3], 'answer': parts[4], 'explanation': parts[5]})
        return questions
    except Exception as e:
        print(f"Error loading questions: {e}")
        return []

# 問題をファイルに保存する関数
def save_questions(questions):
    try:
        with open('quiz_questions.txt', 'w', encoding='utf-8') as file:
            for i,q in enumerate(questions):
                if i<5:
                    print("q=",q)
                file.write(f"{q['Q_no']}\n{q['genre']}\n{q['title']}\n{q['choices']}\n{q['answer']}\n{q['explanation']}\n\n")
    except Exception as e:
        print(f"Error saving questions: {e}")

@app.route('/q_list')
def q_list():
    questions = load_questions()
    # print("=====",questions)
    return render_template('q_list.html', questions=questions)

@app.route('/editQuiz')
def editQuiz():
    questions = load_questions()
    return render_template('q_list.html', questions=questions)

@app.route('/edit/<int:question_id>', methods=['GET', 'POST'])
def edit_question(question_id):
    questions = load_questions()
    if request.method == 'POST':
        # フォームからデータを取得して更新
        questions[question_id]['title'] = request.form['title']
        questions[question_id]['choices'] = request.form['choices']
        questions[question_id]['answer'] = request.form['answer']
        questions[question_id]['explanation'] = request.form['explanation']
        save_questions(questions)
        return redirect(url_for('admin'))
    return render_template('edit.html', question=questions[question_id], question_id=question_id)

@app.route('/createQuiz')
def index2():
    return render_template('q_index.html')

@app.route('/createQuiz2',methods = ['POST'])
def createQuiz2():
    title = request.form.get('title')
    genre = request.form.get('genre')
    choices = request.form.get('choices')
    answer = request.form.get('answer')
    explanation = request.form.get('explanation') or "なし"  # 空の場合はデフォルト値

    print(f"Received: title={title}, choices={choices}, answer={answer}, explanation={explanation}")

    # 新しい問題を作成
    questions = load_questions()
    new_question = {
        'Q_no': str(len(questions)),
        'genre': genre,
        'title': title,
        'choices': choices,
        'answer': answer,
        'explanation': explanation
    }

    print("New question to save:", new_question)

    # 問題をリストに追加し保存
    questions.append(new_question)
    save_questions(questions)
    return "登録が完了しました"

if __name__ == '__main__':
    app.run(debug=True)

