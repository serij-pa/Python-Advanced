from module_21_orm_2.homework.city_library import app

from models.create_tables_and_insert_data import BookLibrary



if __name__ == '__main__':

    BookLibrary.drop_and_create_tables()
    BookLibrary.insert_authors_and_books()
    BookLibrary.insert_students()
    BookLibrary.insert_receiving_books()
    BookLibrary.select_from_database()
    app.run()