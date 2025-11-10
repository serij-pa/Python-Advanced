from flask import Flask

app = Flask(__name__)

@app.route("/hello/<user>")

def h_w(user: str):
    return f"Привет {user}"

if __name__ == '__main__':
    app.run(debug=True)
