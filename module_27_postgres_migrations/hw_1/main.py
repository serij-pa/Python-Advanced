from flask import Flask
from models import Base, User
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select

app = Flask(__name__)

engine = create_engine(
    "postgresql+psycopg2://postgres:postgres@postgres_cont:5432/postgres", echo=True
)

data_users = [
    User(name="Вася", surname="Петров", telephone="+79991111111"),
    User(name="Петя", surname="Васечкин", telephone="+79992222222"),
    User(name="Маша", surname="Старцева", telephone="+79993333333"),
]

@app.before_request
def before_request_func():
    with Session(engine) as session:
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        session.add_all(data_users)
        session.commit()

@app.route("/")
def hello_world():
    return "Hello world!"

@app.route("/data")
def get_data():
    with Session(engine) as session:
        result = session.scalars(select(User))
        users = result.fetchall()
        list_users = []
        for user in users:
            list_users.append(user.to_json())
        return list_users

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
