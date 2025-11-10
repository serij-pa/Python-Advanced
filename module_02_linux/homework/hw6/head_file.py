"""
Реализуйте endpoint, который показывает превью файла, принимая на вход два параметра: SIZE (int) и RELATIVE_PATH —
и возвращая первые SIZE символов файла по указанному в RELATIVE_PATH пути.

Endpoint должен вернуть страницу с двумя строками.
В первой строке будет содержаться информация о файле: его абсолютный путь и размер файла в символах,
а во второй строке — первые SIZE символов из файла:

<abs_path> <result_size><br>
<result_text>

где abs_path — написанный жирным абсолютный путь до файла;
result_text — первые SIZE символов файла;
result_size — длина result_text в символах.

Перенос строки осуществляется с помощью HTML-тега <br>.

Пример:

/head_file/8/docs/simple.txt
/home/user/module_2/docs/simple.txt 8
hello wo

/head_file/12/docs/simple.txt
/home/user/module_2/docs/simple.txt 12
hello world!
"""

from flask import Flask
import os

app = Flask(__name__)


@app.route("/head_file/<int:size>/<path:relative_path>")
def head_file(size: int, relative_path: str):
    abs_pash = os.path.abspath("war_and_peace.txt")
    with open(relative_path) as book:
        line = book.read(size)

    return f"<h3><i>{abs_pash}</i></h3><br>{len(line)} <br><i>{line}</i>"


if __name__ == "__main__":
    app.run(debug=True)
