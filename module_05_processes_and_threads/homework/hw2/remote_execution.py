"""
Напишите эндпоинт, который принимает на вход код на Python (строка)
и тайм-аут в секундах (положительное число не больше 30).
Пользователю возвращается результат работы программы, а если время, отведённое на выполнение кода, истекло,
то процесс завершается, после чего отправляется сообщение о том, что исполнение кода не уложилось в данное время.
"""
import subprocess
from asyncio import timeout

from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField

app = Flask(__name__)
app.config["WTF_CSRF_ENABLED"] = False


class CodeForm(FlaskForm):
    code = StringField()
    timeout = IntegerField()


def run_python_code_in_subproccess(code: str, timeout: int):
    proc = subprocess.Popen(["pyton", "-c", code], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        outs, errs = proc.communicate(timeout=timeout)
        print(f"Out = {outs}\nErr = {errs}")
    except subprocess.TimeoutExpired:
        proc.kill()
        outs, errs = proc.communicate()
    return outs.decode(), errs.decode(),



@app.route('/run_code', methods=['POST'])
def run_code():
    form = CodeForm()
    if form.validate_on_submit():
        code = form.code.data
        timeout = form.timeout.data
        stdout, stderr = run_python_code_in_subproccess(code=code, timeout=timeout)
        return f"Stdout: {stdout}, stderr: {stderr}"
    return f"Bad request Error = {form.errors}", 400




if __name__ == '__main__':
    app.run(debug=True)
