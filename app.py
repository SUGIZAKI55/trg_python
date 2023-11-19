#11/19 19:34 変更しました。

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home1():
    return "<h1> hello </h1>" 

# @app.route('/aaa')
# def home2():
#     random_number = random.randint(1, 6)
#     print(random_number)

#     if random_number==6:
#         body="大当たり"
#     elif random_number==4 or random_number==5:
#         body="中当たり"
#     else:
#         body="ハズレ"
    
#     return render_template('index.html',body=body)

@app.route('/bbb') #bbbが飛んできたらプログラムが実行
def home3():
    choices = ["10月", "11月", "12月", "11月"]
    # correct_choice_index = 0  # "10月" is the correct choice.
    return render_template('index.html', question="今日は何月か？", choices=choices)

@app.route('/answer', methods=['GET']) #anserが飛んできたら下のプログラムが実行
def check_answer():
    user_choice = request.args.get('choice')
    print(user_choice)
    correct_choice = "10月"

    if user_choice == correct_choice:
        return "正解です！"
    else:
        return "不正解です。"

@app.route('/ccc', methods=['GET'])
def home4():
    print(q1[0])#質問文の表示
    arr = q1[1].split(":")#解答群の作成　多数の中から４つをランダムで選択
    if len(arr)<4:
        crs=len(arr)
    else:
        crs=4    
    result = random.sample(arr, crs)
    print(result)

    cs=q1[2].split(":")
    cors = list(set(result) & set(cs))#正解の作成
    print(cors)

@app.route('/answer2', methods=['POST'])
def check_answer2():
    user_choice = request.forms.get('choice')
    print(user_choice)
    sets=[
    ["問題1 今月は何月ですか？","1月:2月:3月:4月:5月:6月:8月","1月:8月","説明1"],

    ]


if __name__ == "__main__":
    app.run(debug=True,port=8888)
