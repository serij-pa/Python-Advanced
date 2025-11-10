from flask import Flask, request
#from flask_restful import Api, Resource
from flask_restx import Api,Resource
from marshmallow import ValidationError

from models import (
    Book,
    BOOKS,
    AUTHORS,
    get_all_books,
    get_all_authors,
    init_db,
    add_book,
    add_author,
    get_book_by_id,
    delete_book_by_id,
    update_book_by_id,
)
from schemas import BookSchema, AuthorSchema

app = Flask(__name__)
api = Api(app)


class BookList(Resource):
    def get(self) -> tuple[list[dict], int]:
        schema = BookSchema()
        return schema.dump(get_all_books(), many=True), 200

    def post(self) -> tuple[dict, int]:
        data = request.json
        schema = BookSchema()
        try:
            book = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        book = add_book(book)
        return schema.dump(book), 201


class AuthorList(Resource):
    def get(self) -> tuple[list[dict], int]:
        schema = AuthorSchema()
        return schema.dump(get_all_authors(), many=True), 200

    def post(self) -> tuple[dict, int]:
        data = request.json
        schema = AuthorSchema()
        try:
            author = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        author = add_author(author)
        return schema.dump(author), 201


class WorkOnBooks(Resource):
    def get(self, book_id):
        schema = BookSchema()
        return schema.dump(get_book_by_id(book_id)), 200

    def delete(self, book_id):
        schema = BookSchema()
        return schema.dump(delete_book_by_id(book_id)), 200

    def put(self, book_id):
        data = request.json
        book = Book(title=data['title'], author=data['author'], id=book_id)
        return update_book_by_id(book), 200


api.add_resource(BookList, '/api/books')
api.add_resource(AuthorList, '/api/autors')
api.add_resource(WorkOnBooks, '/api/books/<int:book_id>')

if __name__ == '__main__':
    init_db(initial_authors=AUTHORS, initial_books=BOOKS)
    app.run(debug=True)
