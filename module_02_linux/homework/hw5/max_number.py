"""
Реализуйте endpoint, начинающийся с /max_number, в который можно передать список чисел, разделённых слешем /.
Endpoint должен вернуть текст «Максимальное переданное число {number}»,
где number — выделенное курсивом наибольшее из переданных чисел.

Примеры:

/max_number/10/2/19/1
Максимальное число: 10

/max_number/1/1/1/1/1/1/1/2
Максимальное число: 2

"""

from flask import Flask

app = Flask(__name__)


@app.route("/max_number/<path:max_number>")
def max_number(max_number):
    my_list = map(int, max_number.split("/"))
    return f"Максимальное <br> число: <b><i>{max(my_list)}</i></b>"


if __name__ == "__main__":
    app.run(debug=True)
