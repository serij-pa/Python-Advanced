"""
Реализуйте приложение для учёта финансов, умеющее запоминать, сколько денег было потрачено за день,
а также показывать затраты за отдельный месяц и за целый год.

В программе должно быть три endpoints:

/add/<date>/<int:number> — сохранение информации о совершённой в рублях трате за какой-то день;
/calculate/<int:year> — получение суммарных трат за указанный год;
/calculate/<int:year>/<int:month> — получение суммарных трат за указанные год и месяц.

Дата для /add/ передаётся в формате YYYYMMDD, где YYYY — год, MM — месяц (от 1 до 12), DD — число (от 01 до 31).
Гарантируется, что переданная дата имеет такой формат и она корректна (никаких 31 февраля).
"""
from calendar import month

from flask import Flask
from datetime import datetime

app = Flask(__name__)

storage = {}


@app.route("/add/<date>/<int:number>")
def add(date: str, number: int):
    try:
        date_obj = datetime.strptime(date, "%Y%m%d")
        year = date_obj.year
        month = date_obj.month
    except ValueError:
        return "Неверно введена дата"
    if year not in storage:
        storage.setdefault(year, {}).setdefault("total", number)
    else:
        storage[year]["total"] += number
    if month not in storage[year]:
        storage.setdefault(year, {}).setdefault(month, number)
    else:
        storage[year][month] += number
    return f"Траты {storage}"


@app.route("/calculate/<int:year>")
def calculate_year(year: int):
    if year in storage:
        return f"За {year} год было потрачено {storage[year]["total"]}"
    else:
        return f"Трат за {year} год не было"



@app.route("/calculate/<int:year>/<int:month>")
def calculate_month(year: int, month: int):
    if year in storage and month in storage[year]:
        return f"За {month}.{year}г. было потрачено {storage[year][month]}"
    else:
        return f"Трат за {month}.{year}г. не было"


if __name__ == "__main__":
    app.run(debug=True)
