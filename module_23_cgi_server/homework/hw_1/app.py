import json
import re
import time
from wsgiref.simple_server import make_server

class AppNew:

    def __init__(self):
        self.routes = {}

    def route(self, way):
        def decorator(func):
            count = re.search(r'(<)', way)
            endpoint = way[:count.start()] if count is not None else way
            self.routes[endpoint] = func
            return func
        return decorator

    def __call__(self, environ, start_response):
        self.environ = environ
        way = self.environ.get('PATH_INFO')
        headers = [('Content-type', 'application/json')]

        if way == '/hello':
            # URL /hello
            status = '200 OK'
            response = self.routes[way]()
            start_response(status, headers)
            return [json.dumps(response).encode('utf-8')]
        elif way.startswith('/hello'):
            # для /hello/name
            status = '200 OK'
            query = way.split('/')[-1]
            response = self.routes['/hello/'](query)
            start_response(status, headers)
            return [json.dumps(response).encode('utf-8')]
        elif way == '/long_task':
            time.sleep(80)      # задержка в 80 сек
            status = '200 OK'
            html_response = ["<!DOCTYPE html>", "<html>", "<body>", "<h1>Hooray it's working!</h1>",
                             "</body>", "</html>"]
            start_response(status, [('Content-Type', 'text/html')])
            return [line.encode("utf-8") for line in html_response]
        else:
            # при ошибке - показать картинку из /static
            status = '404 Not Found'
            html_response = ["<!DOCTYPE html>", "<html>", "<body>", "<h1>Page not found</h1>",
                             '<img src="static/error_404.jpg" />', "</body>", "</html>"]
            start_response(status, [('Content-Type', 'text/html')])
            return [line.encode("utf-8") for line in html_response]


application = AppNew()

@application.route('/hello')
def welcome():
    return {"response": "Hello, world!"}


@application.route('/hello/<name>')
def welcome_by_name(name):
    return {"response": f"Hello, {name}"}

if __name__ == '__main__':
    server = make_server(host='0.0.0.0', port=5000, app=application)
    print('Сервер запущен по адресу: http://127.0.0.1:5000')
    server.serve_forever()