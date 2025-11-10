from flask import Flask, request
from flask_restful import Api, Resource
from marshmallow import ValidationError

from models import (
    BOOKS,
    AUTORS,
    get_all_books,
    get_all_autors,
    init_db,
    add_book,
    add_autor,
)
from schemas import BookSchema, AutorSchema

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


class AutorList(Resource):
    def get(self) -> tuple[list[dict], int]:
        schema = AutorSchema()
        return schema.dump(get_all_autors(), many=True), 200

    def post(self) -> tuple[dict, int]:
        data = request.json
        schema = AutorSchema()
        try:
            autor = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        autor = add_autor(autor)
        return schema.dump(autor), 201


api.add_resource(BookList, '/api/books')
api.add_resource(AutorList, '/api/autors')

if __name__ == '__main__':
    init_db(initial_autors=AUTORS, initial_books=BOOKS)
    app.run(debug=True)
