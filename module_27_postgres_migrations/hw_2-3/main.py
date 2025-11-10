import json
import time
import requests
from random import randint
from flask import Flask, request
from models import Base, Coffee, User
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select, func

app = Flask(__name__)

engine = create_engine("postgresql+psycopg2://skillbox:skillbox@localhost:5432/skillbox_db", echo=True)

URL_USERS = "https://dummyjson.com/users?limit=5"
URL_COFFEE = "https://dummyjson.com/products/search?q=coffee"

def get_data():
    session = requests.Session()
    users = session.get(URL_USERS).json()
    time.sleep(2)
    coffees = session.get(URL_COFFEE).json()

    list_coffee = []
    for cf in coffees["products"]:
        list_coffee.append(
            Coffee(title=cf["title"], category=cf["category"], description=cf["description"], reviews=[i["comment"] for i in cf["reviews"]]))

    list_users = []
    for us in users:
        list_users.append(
            User(name=us["users"], has_sale=randint(0, 1), address=us["address"], coffee_id=1))

    return list_coffee, list_users


@app.route("/")
def main_page():
    with Session(engine) as session_db:
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        coffee_list, users_list = get_data()
        session_db.add_all(coffee_list)
        session_db.add_all(users_list)
        session_db.commit()
        return "Данные внесены в базу"


@app.route("/add_user", methods=['POST'])
def add_user():
    """POST-запрос http (httpie)
    http://127.0.0.1:5000/add_user name="" address='{"city": "MOSKOW",
    "street": "ENTUZIASTOV", "home_num": 00}' has_sale=1 coffee_id=4
    """
    user_data = request.json
    user = User(
        name=user_data['name'], address=json.loads(user_data['address']),
        has_sale=int(user_data["has_sale"]), coffee_id=int(user_data['coffee_id']))

    with Session(engine) as session_db:
        session_db.add(user)
        session_db.flush()
        data = user.to_json()
        data['coffee_blend'] = user.coffee.title
        session_db.commit()
        return data


@app.route("/search", methods=['POST'])
def search_coffee_by_title():
    """поиска кофе по названию. Полнотекстовый поиск.
    http post http://127.0.0.1:5000/search search_string='Coffee'
    """
    search_string = request.json['search_string']
    with Session(engine) as session_db:
        query = session_db.execute(select(Coffee).where(Coffee.title.match(search_string)))
        coffee = query.scalars().all()
        search_result = []
        for c in coffee:
            search_result.append(c.to_json())
    return search_result


@app.route("/unique")
def get_list_unique_reviews():
    """Список уникальных обзоров к кофе.
    http http://127.0.0.1:5000/unique
    """
    with Session(engine) as session_db:
        unique_reviews = session_db.query(func.unnest(Coffee.reviews)).distinct().all()
        data = {}
        for review in unique_reviews:
            data["unique_list_reviews"] = data.get("unique_list_reviews", []) + [review[0]]
        data["quantity_reviews"] = len(unique_reviews)
        return data


@app.route("/users_from", methods=['POST'])
def get_list_users_from_country():
    """
    Список пользователей, проживающих в стране (страна — входной параметр)
    Example post query:
    http post http://127.0.0.1:5000/users_from country='Germany'
    """
    country = request.json['country']
    with Session(engine) as session_db:
        result = session_db.execute(
            select(User).where(User.address["country"].astext.match(country))
        ).scalars().all()
        list_users = []
        for u in result:
            list_users.append(u.to_json())
    return list_users


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)