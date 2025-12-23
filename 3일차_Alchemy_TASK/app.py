from flask import Flask
from flask_smorest import Api
from db import db
from models import User, Board

app = Flask(__name__)

#데이터베이스와 연결 (SQLALCHEMY를 이용해)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:20001208@localhost/lms'
#메모리 영역에서 객체가 바뀔때마다 그것들을 TRACKING 할꺼냐?
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

#blueprint설정 smorest에서 blueprint불러와서 swagger적용 가능
app.config["API_TITLE"] = "My API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.1.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)

from routes.board import board_blp
from routes.user import user_blp
#블루프린트 등록
api.register_blueprint(board_blp)
api.register_blueprint(user_blp)

#라우트 정의
from flask import render_template
@app.route('/manage-boards')
def manage_boards():
    return render_template('boards.html')

@app.route('/manage-users')
def manage_users():
    return render_template('users.html')

#db가 생성되있으면 그대로가고 아니면 pass
if __name__ == '__main__':
    with app.app_context():
        #models.py에 두개의 모델이 테이블로 만들어짐 밑에 코드한줄이
        db.create_all()
    app.run(debug=True)