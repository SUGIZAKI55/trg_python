from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/greet/<int:user_id3>')
def greet(user_id3):
    print(user_id3+1)
    # user_id を受け取り、それをレスポンスに含める
    # return render_template_string('<h1>Hello, user {{ user_id }}!</h1>', user_id=user_id)
    return render_template_string('<h1>Hello, user {{ user_id3 }}!</h1>', user_id3=user_id3)
if __name__ == '__main__':
    app.run(debug=True)

