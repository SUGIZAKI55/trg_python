import random
from flask import Flask, redirect, url_for, render_template, request,session
from flask_session import Session
#通常クライアント側にデータが保存される（session）、サーバー側に保存する場合が(Session)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

sets = [
    ["問題1 今月は何月ですか？", "6月:7月:8月:9月:10月:11月:12月", "10月", "説明1"],
    ["問題2 以下の動物の中で鳥はどれ？", "ライオン:象:ペンギン:カンガルー:カモメ:スズメ", "ペンギン:カモメ:スズメ", "ペンギンは鳥の一種ですが、飛べません。"],
    ["問題3 最も大きな惑星は？", "地球:火星:木星:金星", "木星", "木星は太陽系で最も大きな惑星です。"],
    ["問題4 日本の首都は？", "大阪:東京:福岡:仙台", "東京", "日本の首都は東京です。"],
    ["問題5 以下の中で果物はどれ？", "ピーマン:キャベツ:ブロッコリー:メロン:パイナップル:バナナ", "メロン:パイナップル:バナナ", "メロン:パイナップル:バナナは果物の一種ですが、野菜としても扱われることが多いです。"],
    ["問題6 以下の言語の中でスペイン語で「こんにちは」は？", "Hello:Bonjour:Halo:Hola", "Hola", "スペイン語で「こんにちは」は「Hola」と言います。"],
]

@app.route('/loginok')
def loginok():
    session["Q_no"] = 0
    return redirect('/question', code=302)

@app.route('/question') #questionが飛んできたらプログラムが実行
def q1():
    if 'username' not in session:
        print("セッションがありません")
    else:
        print(f"@27= {session=}")
        Q_no = session["Q_no"]
        print("Q_no=",Q_no)
        q1 = sets[Q_no]
        
        # q1= ["問題1 今月は何月ですか？", "6月:7月:8月:9月:10月:11月:12月", "10月", "説明1"]
        print(q1[0])  # 質問文の表示

        arr = q1[1].split(":")  # 解答群の作成　多数の中から４つをランダムで選択
        print("arr=",arr)
        if len(arr) < 4:
            crs = len(arr)
        else:
            crs = 4    
        result = random.sample(arr, crs)
        
        for i, choice in enumerate(result, 1):
            print(i, choice)
        
        cs_temp = set(q1[2].split(":")) #正解をここで作っておく
        correct_choices = set(result) & cs_temp
        session["correct_ans"] = correct_choices
        return render_template('index.html', question=q1[0], choices=result)

@app.route('/answer', methods=['GET']) #answerが飛んできたら下のプログラムが実行
def check_answer():
    correct_ans=session["correct_ans"]
    print("correct_ans=",correct_ans)
    user_choice = request.args.getlist('choice[]')  
    print("user_choice=",user_choice)

    correct_set = correct_ans 
    user_set = set(user_choice) #右がbefore、左はafter

    if user_set == correct_set:
        print("正解")
        answer = "正解"
    else:
        print("不正解。正しい答えは:", correct_ans)
        answer = "不正解"
    #Qをプラス
    Q = session["Q_no"]
    Q = Q + 1
    session["Q_no"]=Q
    return render_template('kekka.html', kekka=answer,Q_no=Q)
    # return answer

    #10/15の作業
    #anserの複数の答えを一致させるプログラムを作成する
    #10/22の作業
    #問題1から問題2へ偏移させるためのプログラムを作成する
    #10/29
    #render_templateを使ってhtmlに変数を渡せる
    #辞書、配列、集合型

    # user_choice = request.args.get('choice')
    # print(user_choice)
    # correct_choice = "10月"

    # if user_choice == correct_choice:
    #     return "正解です！"
    # else:
    #     return "不正解です。"

users = {
    'user1': 'pass1',
    'user2': 'pass2',
}
#users["user2"]=結果がpass2

@app.route('/')
def login_form():
    # GETリクエストの処理: ログインフォームを表示
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    # POSTリクエストの処理: ログインフォームからのデータを処理
    username = request.form['username']
    password = request.form['password'] #userが入れたPassword

    pwd = users.get(username) #ServerがもっているPassword
    #if user_password_hash and check_password_hash(user_password_hash, password):
    #if user_password_hash and user_password_hash=='pass':

    if password == pwd: 
        print("@111 OK")
        # ログイン成功
        session['username'] = username
        print(f"{session ['username']=}")
        #print(f"{session=}")
        return redirect(url_for('loginok'))  # ホームページにリダイレクト
    else:
        return render_template("error.html")


if __name__ == "__main__":
    app.run(debug=True,port=8888)
