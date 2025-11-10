from flask import Flask, render_template, request, redirect
from typing import List

from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField
from wtforms.validators import InputRequired

from models import (init_db, get_all_books, DATA, add_new_book,
                    search, create_table_description_book,
                    DESCRIPTION_BOOK, about,
                    get_all_abouts)

app: Flask = Flask(__name__)


class FormAdd(FlaskForm):
    title = StringField(validators=[InputRequired()])
    author = StringField(validators=[InputRequired()])


class SearchAuthor(FlaskForm):
    author = StringField(validators=[InputRequired()])


def _get_html_table_for_books(books: List[dict]) -> str:
    table = """
<table>
    <thead>
    <tr>
        <th>ID</td>
        <th>Title</td>
        <th>Author</td>
    </tr>
    </thead>
    <tbody>
        {books_rows}
    </tbody>
</table>
"""
    rows: str = ''
    for book in books:
        rows += '<tr><td>{id}</tb><td>{title}</tb><td>{author}</tb></tr>'.format(
            id=book['id'], title=book['title'], author=book['author'],
        )
    return table.format(books_rows=rows)


@app.route('/books')
def all_books() -> str:
    #abouts = get_all_abouts()
    return render_template(
        'index.html',
        books=get_all_books(), abouts=get_all_abouts()
    )


@app.route('/books/form', methods=['POST','GET'])
def get_books_form():
    form = FormAdd()
    if request.method == 'POST':
        if form.validate_on_submit():
            title = form.title.data
            author = form.author.data
            data = title, author
            add_new_book(data)
        return redirect('/books')
    else:
        return render_template(
            'add_book.html',
            form=form)


@app.route('/books/author', methods=['POST','GET'])
def search_author():
    form = SearchAuthor()
    if request.method == 'POST':
        if form.validate_on_submit():
            author = form.author.data
            return render_template('find_book.html', books=search(author))

    else:
        return render_template(
            'author.html',
            form=form)


@app.route('/books/<int:id_book>')
def get_about(id_book: int):
    return render_template('about.html', book=about(id_book))



if __name__ == '__main__':
    app.config["WTF_CSRF_ENABLED"] = False
    init_db(DATA)
    create_table_description_book(DESCRIPTION_BOOK)
    app.run(debug=True)
