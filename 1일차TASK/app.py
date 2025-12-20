from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    users = [
    {"username": "traveler", "name": "Alex"},
    {"username": "photographer", "name": "Sam"},
    {"username": "gourmet", "name": "Chris"}
]
#(1)rendering할 html 파일명 입력
#(2)html로 넘겨줄 데이터 입력
    return render_template('index.html', users=users)

if __name__ == "__main__":
    # debug=True를 넣으면 서버를 껏다켰다 안해도 반영이 된다.
    app.run(debug=True)