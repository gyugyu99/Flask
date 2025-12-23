from flask import jsonify, request
from flask_smorest import Blueprint
from flask.views import MethodView
from db import db
from models import Board

board_blp = Blueprint('Boards', 'boards', description='Opertions on boards', url_prefix='/board')

# API list
# 전체 게시글 불러오기 (GET)
# 게시글 작성 (POST)
@board_blp.route('/')
class BoardList(MethodView):
    def get(self):
        #전체게시글 가져오는 ORM 쿼리
        boards = Board.query.all()
        
        #데이터들을 하나씩 가져와야함 (쿼리셋)
        #가져와서 각각 접근을한거
        # for board in boards:
        #     print('id', board.id)
        #     print('title', board.title)
        #     print('content', board.content)
        #     print('user_id', board.user_id)
        #     #join쿼리로 가져온거랑 다름없음 밑에 SELCT * FROM user LEFT JOIN ...
        #     print('author_name', board.author.name) #user name접근가능
        #     print('author_email', board.author.email) #user email접근가능

        return jsonify([{"id":board.id, 
                        'title':board.title, 
                        'content':board.content,
                        'user_id':board.author.id,
                        'author_name':board.author.name,
                        'author_email':board.author.email} for board in boards])

    def post(self):
        data = request.json
        new_board = Board(title=data['title'], content=data['content'], user_id=data['user_id'])

        db.session.add(new_board)
        db.session.commit()

        return jsonify({'msg': 'success'}), 201
    

# /board/<int:board_id>

# 하나의 게시글 불러오기(GET)
# 특정 게시글 수정하기(PUT)
# 특정 게시글 삭제하기(DElETE)
@board_blp.route("/<int:board_id>")
class BoardResource(MethodView):
    def get(self, board_id):
        board = Board.query.get_or_404(board_id)

        return jsonify({'id' : board.id,
                        'title':board.title,
                        'content':board.content,
                        'author_name': board.author.name
                        })

    def put(self, board_id):
        board = Board.query.get_or_404(board_id)

        data = request.json

        board.title = data['title']
        board.content = data['content']

        db.session.commit()

        return jsonify({'msg':'successfully updated board data'}), 201
        


    def delete(self, board_id):
        board = Board.query.get_or_404(board_id)

        db.session.delete(board)
        db.session.commit()

        return jsonify({"msg": "successfully delete board data"}), 204
