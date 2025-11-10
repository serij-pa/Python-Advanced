import sqlite3
import csv


def delete_wrong_fees(
        cursor: sqlite3.Cursor,
        wrong_fees_file: str
) -> None:
    with open(wrong_fees_file) as csv_file:
        cars = csv.reader(csv_file)
        number_cars = []
        for car in cars:
            if car[0] != "car_number":
                number_cars.append(car[0])
        tuple_number_cars = tuple(number_cars)
        del_num_car = f"DELETE FROM table_fees WHERE truck_number IN {tuple_number_cars}"
        cursor.execute(del_num_car)
        print(f"Данные об ошибочных штрафах удалены.")


if __name__ == "__main__":
    with sqlite3.connect("../homework.db") as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        delete_wrong_fees(cursor, "../wrong_fees.csv")
        conn.commit()
