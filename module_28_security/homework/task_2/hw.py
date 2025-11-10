from flask import Flask, Response

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<h1>
Чтобы не сработал код ниже:<br>
http://127.0.0.1?query=&ltscript&gtalert("Hacked")&lt/script&gt
<br><br>
Необходимо вставить обработчик заголовков:<br>
response.headers['Content-Security-Policy'] = "default-src 'self'"
<br>
Завернутый в декоратор after_request
<br></h1>
<pre>
@app.after_request
def add_csp(response: Response):
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response
</pre>

</body>
</html>
"""

@app.route("/")
def get_index():
    return HTML


@app.after_request
def add_csp(response: Response):
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response

if __name__ == '__main__':
    app.run()