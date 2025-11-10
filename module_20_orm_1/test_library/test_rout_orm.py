from flask import Flask, jsonify, request, render_template
from test_mod_orm import Base, engine, session, Book, Student, Author, ReceivingBook
from datetime import datetime
from sqlalchemy import update

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index_orm.html')


@app.before_request
def before_request_func():
   Base.metadata.create_all(engine)


@app.route("/books", methods=['GET',])
def get_books():
    books = session.query(Book).all()
    list_books = []
    for book in books:
        list_books.append(book.to_json())
    session.close()
    return render_template('list_books_orm.html', books=list_books)


@app.route("/authors", methods=['GET',])
def get_authors():
    authors = session.query(Author).all()
    list_authors = []
    for author in authors:
        list_authors.append(author.to_json())
    session.close()
    #return jsonify(list_authors=list_authors), 200
    return render_template('list_authors_orm.html', authors=list_authors)


@app.route('/add_book', methods=['POST', 'GET'])
def add_book():
    '''Добавить новую книгу'''
    if request.method == 'POST':
        name = request.form.get('name', type=str)
        count = request.form.get('count', type=int)
        release_date = datetime.strptime(request.form.get('release_date'), '%Y-%m-%d')
        author_id = request.form.get('author_id', type=str)
        new_book = Book(name=name, count=count, release_date=release_date, author_id=author_id)
        session.add(new_book)
        session.commit()
        session.close()
        return 'Книга успешно создана', 201
    #return render_template('add_book.html')


@app.route('/add_author', methods=['POST', 'GET'])
def add_author():
    '''Добавить нового автора'''
    if request.method == 'POST':
        name = request.form.get('name', type=str)
        surname = request.form.get('surname', type=str)
        new_author = Author(name=name, surname=surname)
        session.add(new_author)
        session.commit()
        session.close()
        return 'Автор успешно создан', 201
    return render_template('add_author.html')


@app.route("/students", methods=['GET',])
def get_students():
    students = session.query(Student).all()
    list_students = []
    for student in students:
        list_students.append(student.to_json())
    session.close()
    return jsonify(list_students=list_students), 200
    #нету return render_template('list_students_orm.html', students=list_students)


@app.route('/add_student', methods=['POST', 'GET'])
def add_student():
    '''Добавить нового студента'''
    if request.method == 'POST':
        name = request.form.get('name', type=str)
        surname = request.form.get('surname', type=str)
        phone = request.form.get('phone', type=str)
        email = request.form.get('email', type=str)
        average_score = request.form.get('average_score', type=str)
        select = request.form.get("scholarship")
        if select == "yes":
            scholarship = True
        else:
            scholarship = False
        new_students = Student(name=name, surname=surname, phone=phone, email=email, average_score=average_score, scholarship=scholarship)
        session.add(new_students)
        session.commit()
        session.close()
        return 'Студент успешно создан', 201
    #return render_template('add_students.html')


@app.route('/take_book', methods=['POST', 'GET'])
def take_book():
    '''Забрать книгу'''
    if request.method == 'POST':
        book_id = request.form.get('book_id', type=int)
        student_id = request.form.get('student_id', type=int)
        date_of_return = datetime.strptime(request.form.get('date_of_return'), '%Y-%m-%d')
        new_take_book = ReceivingBook(book_id=book_id, student_id=student_id, date_of_return=date_of_return)
        session.add(new_take_book)
        book = session.query(Book).filter(Book.id == book_id).one_or_none()
        session.execute(update(Book).filter(Book.id == book_id).values(count=book.count - 1))
        session.commit()
        session.close()
        return 'Книгу забрали', 201
    #return render_template('add_receiving_book.html')


@app.route('/return_book', methods=['POST', 'GET'])
def return_book():
    '''Вернуть книгу'''
    if request.method == 'POST':
        book_id = request.form.get('book_id', type=int)
        student_id = request.form.get('student_id', type=int)
        book_returned = ""
        query = session.query(ReceivingBook).filter(
            ReceivingBook.book_id == book_id and ReceivingBook.student_id == student_id
        ).one_or_none()
        if query:
            book = session.query(Book).filter(Book.id == book_id).one_or_none()
            session.execute(update(Book).filter(Book.id == book_id).values(count=book.count + 1))
            session.query(ReceivingBook).filter(ReceivingBook.id == query.id).delete()
            session.commit()
            session.close()
            return 'Книгу сдали'
        else:
            return "Такую книгу студент не брал"
    #return render_template('return_book.html')


@app.route("/receiving_books", methods=['GET',])
def get_receiving_books():
    receiving_books = session.query(ReceivingBook).all()
    list_books = []
    for book in receiving_books:
        list_books.append(book.to_json())
    session.close()
    return jsonify(list_books=list_books), 200
    #нету return render_template('receiving_books.html', list_books=list_books)


@app.route("/debtors", methods=['GET',])
def get_debtors():
    debts = session.query(ReceivingBook).all()
    list_debtors = []
    for debt in debts:
        if debt.coutn_date_with_book > 14:
            student = session.query(Student).filter(Student.id == debt.student_id).one_or_none()
            list_debtors.append(student.to_json())
    session.close()
    return jsonify(list_debtors=list_debtors), 200
    #нету return render_template('receiving_books.html', list_books=list_books)


if __name__ == '__main__':
    app.run()