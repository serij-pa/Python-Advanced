import datetime, random, re
from flask import Flask

app = Flask(__name__)
my_list = ["Chevrolet", "Renault", "Ford", "Lada"]
my_cats = ["корниш-рекс", "русская голубая", "шотландская вислоухая", "мейн-кун", "манчкин"]


@app.route('/hello_world')
def test_function():
    now = datetime.datetime.now().utcnow()
    return f'Привет, мир! сгенерирован в {now}'


@app.route("/cars")
def cars():
    list_avto = ", ".join(my_list)
    return f"Список авто - {list_avto}"


@app.route('/cats')
def cats():
    result_random = random.choice(my_cats)
    return f"Случайная порода из списка - {result_random}"


@app.route('/get_time/now')
def get_time_now():
    now = datetime.datetime.now().utcnow()
    return f"Точное время - {now}"


@app.route('/get_time/future')
def get_time_future():
    delta = datetime.timedelta(hours=1)
    dt = datetime.datetime.now()
    dt1 = dt + delta
    return f"Точное время через час - {dt1}"


@app.route('/get_random_word')
def get_random_word():
    random_word = random.choice(re.findall(r"\w+", list_word))
    return f"Случайное слово из книги «Война и мир» Льва Толстого -- {random_word}"
    pass


@app.route('/counter')
def counter(state=[]):
    if not state:
        state.append(0)
    state[0] += 1
    now = datetime.datetime.now().utcnow()
    return f'Hello, world! {now}\nВызов функции {state[0]}'

with open("war_and_peace.txt", "r", encoding="utf-8") as date:
    list_word = date.read()

if __name__ == '__main__':
    app.run(debug=True)
