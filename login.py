import random
from flask import Flask, redirect, url_for, render_template, request,session
from flask_session import Session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

users = {
    'user1': 'pass1',
    'user2': 'pass2',
}

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

@app.route('/loginok', methods=['GET'])
def loginok():
    print("ログインが無事できました")
    return render_template("loginok.html")

if __name__ == "__main__":
    app.run(debug=True,port=8888)