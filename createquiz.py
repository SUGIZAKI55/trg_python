from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 問題をファイルから読み込む関数
def load_questions():
    with open('quiz_questions.txt', 'r', encoding='utf-8') as file:
        lines = file.read().split('\n\n') #ファイルを読んで、2改行があったら分ける　#配列として分割する関数split \nは改行コード
    print(f"@=9====={lines=}") #=はlinesという変数名も表示する
    questions = [] #四角カッコは配列
    for line in lines: #linesから1こ取り出しlineに入る　複数形を個別する時に使う表記
        print(f"@=11====={line=}")
        parts = line.split('\n')
        if len(parts) == 4:
            questions.append({'title': parts[0], 'choices': parts[1], 'answer': parts[2], 'explanation': parts[3]})
    return questions

# 問題をファイルに保存する関数
def save_questions(questions):
    with open('quiz_questions.txt', 'w', encoding='utf-8') as file:
        for q in questions:
            file.write(f"{q['title']}\n{q['choices']}\n{q['answer']}\n{q['explanation']}\n\n")

@app.route('/editQuiz')
def index():
    questions = load_questions()
    return render_template('e_index.html', questions=questions)

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
        return redirect(url_for('index'))
    return render_template('edit.html', question=questions[question_id], question_id=question_id)

@app.route('/createQuiz')
def index2():
    questions = load_questions()
    return render_template('q_index.html', questions=questions)

if __name__ == '__main__':
    app.run(debug=True)
