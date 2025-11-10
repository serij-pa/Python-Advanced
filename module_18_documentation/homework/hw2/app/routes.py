from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flasgger import APISpec, Swagger
from flasgger import swag_from
from flask import Flask, request
#from flask_restful import Api, Resource
from flask_restx import Api,Resource
from marshmallow import ValidationError
from werkzeug.serving import WSGIRequestHandler

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
    get_book_by_author,
    delete_author_by_id,
)
from schemas import BookSchema, AuthorSchema

app = Flask(__name__)
api = Api(app)


class BookList(Resource):
    @swag_from("documentation/books_get.yml")
    def get(self) -> tuple[list[dict], int]:
        schema = BookSchema()
        return schema.dump(get_all_books(), many=True), 200

    @swag_from("documentation/books_post.yml")
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
    @swag_from("documentation/books_get_id.yml")
    def get(self, book_id):
        schema = BookSchema()
        return schema.dump(get_book_by_id(book_id)), 200

    @swag_from("documentation/books_delete_id.yml")
    def delete(self, book_id):
        schema = BookSchema()
        return schema.dump(delete_book_by_id(book_id)), 200

    @swag_from("documentation/books_put_id.yml")
    def put(self, book_id):
        data = request.json
        book = Book(title=data['title'], author=data['author'], id=book_id)
        return update_book_by_id(book), 200


class Authors(Resource):
    def get(self, author_id):
        schema = BookSchema()
        return schema.dump(get_book_by_author(author_id), many=True), 200

    def delete(self, author_id):
        schema = AuthorSchema()
        return schema.dump(delete_author_by_id(author_id)), 200


swagger = Swagger(app, template_file='documentation/spes_authors.json')

api.add_resource(BookList, '/api/books')
api.add_resource(AuthorList, '/api/authors')
api.add_resource(WorkOnBooks, '/api/books/<int:book_id>')
api.add_resource(Authors, '/api/authors/<int:author_id>')

if __name__ == '__main__':
    init_db(initial_authors=AUTHORS, initial_books=BOOKS)
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    app.run(debug=True)
