#Model -> Table생성
#게시글 - board
#유저 - user
#단수 복수 확인
from db import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable =False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    #역참조 board에서 author를 역참조 'back_populates'
    #lazy='dynamic' 이 쿼리셋은 한번에 모든 데이터 안가져옴
    #하나씩 가져올 수 있게함 (컬럼에는 추가안됨)
    boards = db.relationship('Board', back_populates='author', lazy='dynamic')

class Board(db.Model):
    __tablename__ = "boards"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(300))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
#    (얘도 컬럼에는 추가안됨))
    author = db.relationship('User', back_populates='boards')