from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST']) #добавили методы
def hello_world():
    if request.method == 'POST':
         print(request.form['username'])
         print(request.form['password'])
         return 'Hello POST world!'

    else:
         return render_template('hellow_world.html')

app.run()