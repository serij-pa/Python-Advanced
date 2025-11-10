from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import select
from datetime import datetime

from . import engine, session_factory
from models import Base, Author, Book, Student, ReceivingBook


class BookLibrary:
    @staticmethod
    def drop_and_create_tables():
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)


    @staticmethod
    def insert_authors_and_books():
        with session_factory() as session:
            # Добавим авторов
            # Александр Пушкин
            author_1 = Author(name="Александр", surname="Пушкин")
            book_1 = Book(
                title="Евгений Онегин", count=5,
                release_date=datetime.strptime('1831-10-05', '%Y-%m-%d'),)

            book_2 = Book(
                title="Руслан и Людмила", count=10,
                release_date=datetime.strptime('1820-04-07', '%Y-%m-%d'))

            book_3 = Book(
                title="Сказка о рыбаке и рыбке", count=15,
                release_date=datetime.strptime('1833-10-14', '%Y-%m-%d'))

            author_1.books.append(book_1)
            author_1.books.append(book_2)
            author_1.books.append(book_3)

            author_2 = Author(name="Михаил", surname="Булгаков")

            book_4 = Book(
                title="Собачье сердце", count=20,
                release_date=datetime.strptime('1925-01-01', '%Y-%m-%d'),)

            book_5 = Book(
                title="Белая гвардия", count=22,
                release_date=datetime.strptime('1925-11-21', '%Y-%m-%d'),)

            book_6 = Book(
                title="Мастер и Маргарита", count=27,
                release_date=datetime.strptime('1928-05-15', '%Y-%m-%d'),)

            author_2.books.append(book_4)
            author_2.books.append(book_5)
            author_2.books.append(book_6)

            author_3 = Author(name="Иван", surname="Бунин")

            book_7 = Book(
                title="Тёмные аллеи", count=14,
                release_date=datetime.strptime('1938-02-17', '%Y-%m-%d'),)

            book_8 = Book(
                title="Митина любовь", count=17,
                release_date=datetime.strptime('1925-12-10', '%Y-%m-%d'),)

            book_9 = Book(
                title="Дело корнета Елагина", count=19,
                release_date=datetime.strptime('1938-02-17', '%Y-%m-%d'),)

            author_3.books.append(book_7)
            author_3.books.append(book_8)
            author_3.books.append(book_9)

            session.add_all([author_1, author_2, author_3])
            session.commit()


    @staticmethod

    def insert_students():

        with session_factory() as session:

            student_1 = Student(name="Иван", surname="Иванов", phone="+79021111111", email="ivan@gmail.com", average_score=1)
            student_2 = Student(name="Пётр", surname="Петров", phone="+79022222222", email="pyotr@gmail.com", average_score=2)
            student_3 = Student(name="Александр", surname="Александров", phone="+79023333333", email="alex@gmail.com", average_score=3)
            student_4 = Student(name="Мария", surname="Машкина", phone="+79024444444", email="maria@gmail.com", average_score=4)
            student_5 = Student(name="Василий", surname="Васильев", phone="+790215555555", email="vasiliy@gmail.com", average_score=5)
            student_6 = Student(name="Ольга", surname="Ольгина", phone="+79026666666", email="olga@gmail.com", average_score=5)
            student_7 = Student(name="Людмила", surname="Грачева", phone="+79027777777", email="ludmila@gmail.com", average_score=6)
            student_8 = Student(name="Кирилл", surname="Воробьев", phone="+79028888888", email="kirill@gmail.com", average_score=5)
            student_9 = Student(name="Николай", surname="Синицин", phone="+79029999999", email="nikoay@gmail.com", average_score=3)
            student_10 = Student(name="Глеб", surname="Чижиков", phone="+79020000000", email="gleb@gmail.com", average_score=7)
            session.add_all([student_1, student_2, student_3, student_4, student_5, student_6, student_7, student_8, student_9, student_10])

            session.commit()


    @staticmethod

    def insert_receiving_books():

        with session_factory() as session:

            rb_1 = ReceivingBook(student_id=1, book_id=1, date_of_issue='2024-04-01', date_of_return='2024-04-15')
            rb_2 = ReceivingBook(student_id=2, book_id=3, date_of_issue='2024-05-10', date_of_return='2024-05-21')
            rb_3 = ReceivingBook(student_id=3, book_id=2, date_of_issue='2024-06-01')
            rb_4 = ReceivingBook(student_id=4, book_id=1, date_of_issue='2024-04-01', date_of_return='2024-04-15')
            rb_5 = ReceivingBook(student_id=5, book_id=6, date_of_issue='2024-06-01')
            rb_6 = ReceivingBook(student_id=6, book_id=2, date_of_issue='2024-05-01', date_of_return='2024-05-15')
            rb_7 = ReceivingBook(student_id=7, book_id=6, date_of_issue='2024-06-01')
            rb_8 = ReceivingBook(student_id=7, book_id=3, date_of_issue='2024-01-01', date_of_return='2024-04-15')
            rb_9 = ReceivingBook(student_id=7, book_id=2, date_of_issue='2024-02-01', date_of_return='2024-04-21')
            rb_10 = ReceivingBook(student_id=10, book_id=1, date_of_issue='2024-01-01', date_of_return='2024-01-15')
            rb_11 = ReceivingBook(student_id=1, book_id=3, date_of_issue='2024-01-01', date_of_return='2024-04-15')
            rb_12 = ReceivingBook(student_id=1, book_id=2, date_of_issue='2024-02-01', date_of_return='2024-04-21')
            rb_13 = ReceivingBook(student_id=1, book_id=5, date_of_issue='2024-01-01', date_of_return='2024-01-15')

            session.add_all([rb_1, rb_2, rb_3, rb_4, rb_5, rb_6, rb_7, rb_8, rb_9, rb_10, rb_11, rb_12, rb_13])
            session.commit()


    @staticmethod

    def select_from_database():

        with session_factory() as session:
            result = session.execute(select(Author)).unique()
            authors = result.all()
            result = session.execute(select(Book))
            books = result.all()
            result = session.execute(select(Student)).unique()
            students = result.all()
            # result = session.execute(select(ReceivingBooks))
            # receiving_books = result.all()
            print('Авторы книг:')
            for i in authors:
                print(f"ID:{i[0].id} Имя: {i[0].name}, Фамилия: {i[0].surname}")

            print('\nКниги:')
            for i in books:
                print(f"ID:{i[0].id} Название: {i[0].title}. Количество книг: {i[0].count}")

            print('\nСтуденты:')
            for i in students:
                print(f"ID:{i[0].id} Имя: {i[0].name}, Фамилия: {i[0].surname}")

