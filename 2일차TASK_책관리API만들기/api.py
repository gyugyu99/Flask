from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import BookSchema

# url_prefix=  /books라는 url로 접근하는 모든 api를 book_blp에 적용하겠다

book_blp = Blueprint('books', 'books', url_prefix='/books', description='Operations on books')

# 임시 데이터베이스 리스트
books = []

#첫번째 클래스 BookList
@book_blp.route('/')
class BookList(MethodView):

    #many=True를 이용해서 books에 저장되어있는 전체를 보여주는 옵션
    #GET
    @book_blp.response(200, BookSchema(many=True))
    def get(self):
        return books

    #POST와 PUT에 arguments를 옵션으로 BookSchema를 검사 (smorest옵션임 검사하는 옵션)
    @book_blp.arguments(BookSchema) #들어오는거 검사
    @book_blp.response(201, BookSchema) #응답 (나가는거 포장)
    #BookSchema 검증을 통과한 요청 데이터들
    def post(self, new_data):
        #new_data 추가시 books의 길이 +1을 id로 추가
        new_data['id'] = len(books) + 1
        #books리스트에 추가
        books.append(new_data)
        return new_data

#두번째 클래스 Book
@book_blp.route('/<int:book_id>')
class Book(MethodView):
    #get 1개의 데이터만 받음
    @book_blp.response(200, BookSchema)
    def get(self, book_id):
        #next는 조건을 만족하는걸 찾으면 그 값을 반환, 없으면 None을 가져옴
        book = next((book for book in books if book['id'] == book_id), None)
        #None이면 404 에러 반환
        if book is None:
            abort(404, message="Book not found.")
        return book

    @book_blp.arguments(BookSchema) #검증
    @book_blp.response(200, BookSchema) #리턴할때도 검증
    #PUT
    def put(self, new_data, book_id):
        book = next((book for book in books if book['id'] == book_id), None)
        if book is None:
            abort(404, message="Book not found.")
        #유저가 보내준 new_data로 업데이트함
        book.update(new_data)
        return book
    #DELETE
    @book_blp.response(204)
    def delete(self, book_id):
        #클래스 밖의 리스트기때문에 전역 설정
        global books
        book = next((book for book in books if book['id'] == book_id), None)
        if book is None:
            abort(404, message="Book not found.")
        books = [book for book in books if book['id'] != book_id]
        return ''