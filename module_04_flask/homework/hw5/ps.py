"""
Напишите GET-эндпоинт /ps, который принимает на вход аргументы командной строки,
а возвращает результат работы команды ps с этими аргументами.
Входные значения эндпоинт должен принимать в виде списка через аргумент arg.

Например, для исполнения команды ps aux запрос будет следующим:

/ps?arg=a&arg=u&arg=x
"""
import shlex
import string
import subprocess
from typing import List

from flask import Flask, request


app = Flask(__name__)


@app.route("/ps", methods=["GET"])
def _ps() -> str:
    argum: List[str] = request.args.getlist("arg")
    print(f"Argum: {argum}")
    clean_com = shlex.quote("".join(argum))
    print(f"Clean com: {clean_com}")
    clean_cmd = shlex.split(clean_com)
    print(f"Clean cmd: {clean_cmd}")

    result = ["ps"]
    result.extend(clean_cmd)
    print(f"Result: {result}")
    final_result = subprocess.run(result, capture_output=True)
    return f"That's all ...<br> <pre>{final_result}</pre>"

    # arguments_cleaned = [shlex.quote(s) for s in arguments]
    # command_str = f"ps {"".join(arguments_cleaned)}"
    # command = shlex.split(command_str)
    # result = subprocess.run(command, capture_output=True)
    #
    # if result.returncode == 0:
    #     return f"Something went wrong"

    # output = result.stdout.decode()
    # return string.Template(f"<pre>${output}</pre>").substitute(output=output)


if __name__ == "__main__":
    app.run(debug=True)
