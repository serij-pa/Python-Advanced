import calendar, csv, os
from datetime import datetime, date

from flask import Flask, jsonify, request, render_template
from sqlalchemy import update, select, func, delete

from models.models import Base, Book, Student, Author, ReceivingBook
from models.create_tables_and_insert_data import session_factory
from module_21_orm_2.homework.city_library import app


@app.route("/")
def index():
    return render_template('index_21.html')


@app.route("/books")
def get_books():
    with session_factory() as session:
        books = session.execute(select(Book)).all()
        list_books = []
        for book in books:
            list_books.append(book[0].to_json())
        return render_template('list_books_21.html', books=list_books)


@app.route("/authors")
def get_authors():
    with session_factory() as session:
        authors = session.execute(select(Author)).all()
        list_authors = []
        for author in authors:
            list_authors.append(author[0].to_json())
            return render_template('list_authors_21.html', authors=list_authors)


@app.route('/add_book', methods=['POST', 'GET'])
def add_book():
    '''Добавить новую книгу'''
    with session_factory() as session:
        if request.method == 'POST':
            name = request.form.get('name', type=str)
            count = request.form.get('count', type=int)
            release_date = datetime.strptime(request.form.get('release_date'), '%Y-%m-%d')
            author_id = request.form.get('author_id', type=str)
            new_book = Book(title=name, count=count, release_date=release_date, author_id=author_id)
            session.add(new_book)
            session.commit()
            return (f"Книга успешно создана <br><a href='/'>На главную.</a><br>")

        authors = session.execute(select(Author)).unique().all()
        list_authors = []
        for author in authors:
            list_authors.append(author[0].to_json())
        return render_template('add_book_21.html', authors=list_authors)


@app.route('/add_author', methods=['POST', 'GET'])
def add_author():
    '''Добавить нового автора'''
    if request.method == 'POST':
        with session_factory() as session:
            name = request.form.get('name', type=str)
            surname = request.form.get('surname', type=str)
            new_author = Author(name=name, surname=surname)
            session.add(new_author)
            session.commit()
        return (f"Автор успешно создан <br><a href='/'>На главную.</a><br>")
    return render_template('add_author_21.html')


@app.route('/add_student', methods=['POST', 'GET'])
def add_student():
    '''Добавить нового студента'''
    with session_factory() as session:
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
            return (f"Студент успешно создан <br><a href='/'>На главную.</a><br>")
        return render_template('add_student_21.html')


@app.route('/take_book', methods=['POST', 'GET'])
def take_book():
    '''Забрать книгу'''
    with session_factory() as session:
        if request.method == 'POST':
            book_id = request.form.get('book', type=int)
            student_id = request.form.get('student', type=int)
            #date_of_return = datetime.strptime(request.form.get('date_of_return'), '%Y-%m-%d')
            new_take_book = ReceivingBook(book_id=book_id, student_id=student_id, )
            session.add(new_take_book)

            # книга для выдачи студенту
            book = session.query(Book).filter(Book.id == book_id).one_or_none()
            # уменьшаем количество книг
            session.execute(update(Book).filter(Book.id == book_id).values(count=book.count - 1))
            session.commit()

            return (f"Книгу забрали <br><a href='/'>На главную.</a><br>")

        students = session.execute(select(Student.id, Student.name, Student.surname)).unique().all()
        list_students = []
        for student in students:
            list_students.append({"id": student[0], "name": student[1], "surname": student[2]})

        books = session.execute(select(Book.id, Book.title, Book.count)).unique().all()
        list_books = []
        for book in books:
            list_books.append({"id": book[0], "title": book[1], "count": book[2]})

        return render_template('take_book_21.html', students=list_students, books=list_books)


@app.route('/return_book', methods=['POST', 'GET'])
def return_book():
    '''Вернуть книгу'''
    with session_factory() as session:
        if request.method == 'POST':
            book_id = request.form.get('book', type=int)
            student_id = request.form.get('student', type=int)

            book_taken = session.execute(select(ReceivingBook.id).filter(
                ReceivingBook.book_id == book_id, ReceivingBook.student_id == student_id
            )).unique().one_or_none()
            if book_taken:
                book_count = session.execute(select(Book.count).filter(Book.id == book_id)).scalar()
                session.execute(update(Book).filter(Book.id == book_id).values(count=book_count + 1))
                session.execute(update(ReceivingBook).filter(
                    ReceivingBook.id == book_taken[0]).values(date_of_return=datetime.now()))
                session.commit()

                return (f"Книгу сдали  "
                        f"<br><a href='/'>На главную.</a><br>")
            else:
                return (f"Такую книгу студент не брал "
                        f"<br><a href='/'>На главную.</a><br>")

            result = session.execute(select(Student.id, Student.name, Student.surname).where(
                    Student.id.in_(list(chain(*session.execute(select(ReceivingBook.student_id)
                                                               .filter(ReceivingBook.date_of_return == None)).all())))))

            students = result.all()
            list_students = []
            for student in students:
                list_students.append({"id": student[0], "name": student[1], "surname": student[2]})
            # список  взятых студентами
            result = session.execute(select(Book.id, Book.title).where(
                    Book.id.in_(list(chain(*session.execute(select(ReceivingBook.book_id)
                                                            .filter(ReceivingBook.date_of_return == None)).all())))))
            books = result.all()
            list_books = []
            for books_count in books:
                list_books.append({"id": books_count[0], "title": books_count[1]})

            return render_template('return_book_21.html', students=list_students, books=list_books)


@app.route('/books_by_author', methods=['GET', 'POST'])
def get_remains_books_by_author():
    # 1. Получите количество оставшихся в библиотеке книг по автору (GET — входной параметр — ID автора)
    with session_factory() as session:
        if request.method == 'POST':
            author_id = request.form.get('author_id', type=int)
            result = session.execute(select(Book.count).filter_by(author_id=author_id)).all()
            remains_books = 0
            for count in result:
                remains_books += count[0]
            return render_template("show_remaining_books_by_author.html", count=remains_books, id=author_id)
        authors = session.execute(select(Author)).unique().all()
        list_authors = []
        for author in authors:
            list_authors.append(author[0].to_json())
        return render_template('select_author.html', authors=list_authors)


@app.route('/book_recommendation', methods=['GET', 'POST'])
def get_book_recommendation():
    """список книг, которые студент не читал"""
    with session_factory() as session:
        if request.method == 'POST':
            student_id = request.form.get('student_id', type=int)
            books = session.query(ReceivingBook.book_id).filter_by(student_id=student_id)
            authors = session.query(Book.author_id).where(Book.id.in_(books))
            recommend_books = session.query(Book).where(Book.id.not_in(books)).where(Book.author_id.in_(authors))
            books_list = []
            books = recommend_books.all()
            for book in books:
                books_list.append(book.to_json())
            return render_template("book_recommendation.html", books=books_list)

        result = session.execute(select(Student).where(
                Student.id.in_(list(chain(*session.execute(select(ReceivingBook.student_id)).all())))))
        students = result.unique().all()
        students_list = []
        for student in students:
            students_list.append(student[0].to_json())

        return render_template("select_student.html", students=students_list)


@app.route('/count_books', methods=['GET', 'POST'])
def get_count_books_in_month():
    if request.method == 'POST':
        month = request.form.get('month', type=int)
        days = calendar.monthrange(datetime.now().year, month)[1]
        with session_factory() as session:
            books = session.execute(select(ReceivingBook).filter(
                ReceivingBook.date_of_issue.between(
                    date(2024, month, 1), date(2024, month, days))
            )).unique().all()

        return f"Количество книг, которые студенты брали в {month} месяце: {len(books)}"

    months_list = list(range(1, datetime.now().month + 1))
    return render_template("select_month.html", months=months_list)


@app.route('/popular_book')
def get_popular_book():
    with (session_factory() as session):
        books = session.query(
            ReceivingBook.book_id, func.count(ReceivingBook.book_id)
        ).where(ReceivingBook.student_id.in_(
            session.query(Student.id).where(Student.average_score > 4))).group_by(ReceivingBook.book_id).all()

        book_id = max(books, key=lambda book: book[1])[0]
        book_title = session.execute(select(Book.title).filter_by(id=book_id)).first()
    return (f"Самая популярная книга: {book_title[0]}</h3>"
            f"<a href='/'>Вернуться на главную страницу</a>")


@app.route('/top_ten')
def get_top_ten_students():
    with (session_factory() as session):
        students = session.query(Student).where(
            Student.id.in_(session.query(ReceivingBook.student_id).filter(
                ReceivingBook.date_of_issue.between(date(2024, 1, 1), date(2024, 12, 31))
            ).group_by(
                ReceivingBook.student_id).order_by(func.count(ReceivingBook.book_id).desc()).limit(10))).all()
        students_list = []
        for student in students:
            students_list.append(student.to_json())
    return render_template('top_ten_students.html', students=students_list)


@app.route('/load_csv_file', methods=['GET', 'POST'])
def load_csv_file():
    # Загрузка csv-файла, чтение и запись данных в БД
    if request.method == "POST":
        file = request.files['csv_file']
        file.save(os.path.join(file.filename))
        with open(file.filename, "r") as filename:
            fieldnames = ['first_name', 'last_name', 'phone', 'email']
            read_file = csv.DictReader(f=filename, fieldnames=fieldnames, delimiter=";")
            dict_list = []
            for string_ in read_file:
                dict_list.append(string_)
            with session_factory() as session:
                session.bulk_insert_mappings(Student, dict_list)
                session.commit()
        return ("Данные о студентах загружены. <a href='/'>Возврат на главную страницу</a>")

    return render_template("load_csv_file.html")



@app.route('/delete', methods=['GET', 'POST'])
def delete_author():
    # Удалить автора со всеми его книгами
    with session_factory() as session:
        if request.method == 'POST':
            author_id = request.form.get('author_id', type=int)
            session.execute(delete(Author).filter(Author.id == author_id))
            session.commit()

        authors = session.execute(select(Author)).unique().all()
        authors_list = []
        for author in authors:
            authors_list.append(author[0].to_json())
        return render_template("select_author.html", authors=authors_list)