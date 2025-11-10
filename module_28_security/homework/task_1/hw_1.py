from flask import Flask, jsonify, request, Response

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def handler():
    if request.method == "GET":
        print(request.headers)
        return jsonify({"Hello": "User"})
    else:
        print(request.headers)
        return jsonify({"Hello": request.json["name"]})


@app.after_request
def add_cors(response: Response):
    response.headers['Access-Control-Allow-Origin'] = 'https://skillbox.ru'
    response.headers['Access-Control-Allow-Headers'] = 'X-My-Fancy-Header, Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
    return response


if __name__ == '__main__':
    app.run(port=8080, debug=True)

"""
запрос в браузере
fetch('http://127.0.0.1:8080', {method: 'POST', body: JSON.stringify({name: 'Sergey'}), 
headers: {'Content-Type': 'application/json'}}).then(resp => resp.text()).then(console.log)
"""
