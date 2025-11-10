"""
Напишите GET-эндпоинт /uptime, который в ответ на запрос будет выводить строку вида f"Current uptime is {UPTIME}",
где UPTIME — uptime системы (показатель того, как долго текущая система не перезагружалась).

Сделать это можно с помощью команды uptime.
"""
import datetime
import subprocess

from flask import Flask

app = Flask(__name__)


@app.route("/uptime", methods=['GET'])
def uptime() -> str:
    res = subprocess.run(["uptime"], stdout=subprocess.PIPE)
    respons = str(res.stdout).split()
    respons1 = f"Current uptime is {respons[3]} {respons[4][:-1]}"
    print(respons1)

    return respons1
    #return f"Current uptime is {UPTIME}"



if __name__ == '__main__':
    app.run(debug=True)
