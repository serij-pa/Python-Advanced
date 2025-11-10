import datetime

from typing import Annotated
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy import ForeignKey, select, case, func
from module_21_orm_2.homework.city_library.models import session_factory

str_150 = Annotated[str, 150]
str_50 = Annotated[str, 50]
int_pk = Annotated[int, mapped_column(autoincrement=True, primary_key=True)]


class Base(DeclarativeBase):
    __abstract__ = True
    id: Mapped[int_pk]


class Author(Base):
    __tablename__ = "authors"

    name: Mapped[str_50]
    surname: Mapped[str_50]

    def __repr__(self):
        return f"{self.name}, {self.surname}"

    def __getitem__(self, item):
        return getattr(self, item)

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    books = relationship("Book", backref="author", lazy="joined", cascade="all, delete-orphan")


class Book(Base):
    __tablename__ = 'books'

    title: Mapped[str_150]
    count: Mapped[int] = mapped_column(default=1)
    release_date: Mapped[datetime.date]
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id", ondelete="CASCADE"))

    def __repr__(self):
        return f"<Book(id={self.id}, name={self.name}>)"

    def __getitem__(self, item):
        return getattr(self, item)

    def to_json(self):
        to_json = {c.name: f"{getattr(self, c.name)}" for c in self.__table__.columns}
        #print(to_json)
        return to_json


class Student(Base):
    __tablename__ = 'students'

    name: Mapped[str_50]
    surname: Mapped[str_50]
    phone: Mapped[str_50]
    email: Mapped[str_150]
    average_score: Mapped[int | None] #средний балл
    scholarship: Mapped[bool | None] #стипендия

    @classmethod
    def get_student_by_scholarship(cls): # студенты со стипендией
        with session_factory() as session:
            students = session.execute(select(Student)
                                       .filter(Student.scholarship == True)
                                       ).unique().all()
            list_students = []
            for student in students:
                list_students.append(student.to_json)
            return list_students

    @classmethod
    def get_student_by_high_average_score(cls, sent_score): # студенты с средним балом выше переданного
        with session_factory() as session:
            students = session.query(Student).filter(Student.average_score > sent_score).all()
            list_students = []
            for student in students:
                list_students.append(student.to_json)
            return list_students

    def __repr__(self):
        return self.name + "" + self.surname

    def __getitem__(self, item):
        return getattr(self, item)

    def to_json(self):
        to_json = {c.name: f"{getattr(self, c.name)}" for c in self.__table__.columns}
        #print(to_json)
        return to_json

    student_receiving_books = relationship(
        "ReceivingBook",
        back_populates="student_with_book",
        cascade="all, delete-orphan",
        lazy="joined"
    )

    receive = association_proxy("student_receiving_books", "book")


class ReceivingBook(Base):
    __tablename__ = 'receiving_books'

    book_id : Mapped[int] = mapped_column(ForeignKey(
        "books.id",
        ondelete="CASCADE"), primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey(
        "students.id",
        ondelete="CASCADE"), primary_key=True)
    date_of_issue: Mapped[datetime.date] = mapped_column(default=datetime.datetime.now())
    date_of_return: Mapped[datetime.date] = mapped_column(nullable=True)

    @hybrid_property
    def coutn_date_with_book(self):
        end_date = self.date_of_return or datetime.datetime.now()
        return (end_date - self.date_of_issue).days

    @coutn_date_with_book.expression
    def coutn_date_with_book(cls):
        end_date = case((cls.date_of_return != None, cls.date_of_return),
                        else_=func.now())
        return func.julianday(end_date) - func.julianday(cls.date_of_issue)

    def __repr__(self):
        return f"{self.book_id}, {self.student_id}, {self.date_of_issue}, {self.date_of_return}"

    def __getitem__(self, item):
        return getattr(self, item)

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    student_with_book: Mapped["Student"] = relationship(
        back_populates="student_receiving_books",
        cascade="all, delete",
        lazy="joined")

    book: Mapped[Book] = relationship()

