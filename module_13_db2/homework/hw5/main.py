import sqlite3
import random

LEVEL_TEAM = ["слабая", "средняя", "сильная"]
LIST_COUNTRIES = ["Аргентина", "Испания", "Франция", "Англия", "Бразилия", "Нидерланды", "Португалия", "Бельгия", "Италия", "Германия", "Хорватия", "Марокко", "Колумбия", "Уругвай", "Япония", "США", "Мексика", "Иран", "Сенегал", "Швейцария", "Дания", "Корея", "Швеция", "Канада", "Сербия", ]
LIST_COMMANDS = ["Спартак", "Барселона", "Реал", "Бавария", "Манчестер", "Ливерпуль", "Ювентус", "Атлетико", "Интер", "Боруссия", "ПСЖ", "Челси", "Рома", "Сити", "Арсенал", "Наполи", "Фламенго", "Сантос", "Дортмунд", "Плейт", "Флуминенсе", "Коринтианс", "Аль-Хилал", "ль-Иттихад", "Палмейрас"]


def creating_commands():
    team = []
    for i in range(26):
        ls = (random.choice(LIST_COUNTRIES), random.choice(LIST_COMMANDS), random.choice(LEVEL_TEAM))
        team.append(ls)
    return team

#TEAM = creating_commands()
TEAMS = [
    ('Нидерланды', 'Атлетико', 'средняя'), ('Марокко', 'Реал', 'сильная'),
    ('Италия', 'Боруссия', 'средняя'), ('Швейцария', 'ль-Иттихад', 'сильная'),
    ('Иран', 'Флуминенсе', 'средняя'), ('Уругвай', 'Сити', 'средняя'),
    ('Италия', 'Реал', 'сильная'), ('Сербия', 'Атлетико', 'слабая'),
    ('Мексика', 'ль-Иттихад', 'сильная'), ('Уругвай', 'Палмейрас', 'слабая'),
    ('Марокко', 'Интер', 'средняя'), ('Мексика', 'Рома', 'средняя'),
    ('Швейцария', 'Челси', 'средняя'), ('Сербия', 'Манчестер', 'сильная'),
    ('США', 'Манчестер', 'слабая'), ('Англия', 'ль-Иттихад', 'слабая'),
    ('Англия', 'ль-Иттихад', 'средняя'), ('Швеция', 'Ювентус', 'слабая'),
    ('Швеция', 'Наполи', 'слабая'), ('Сенегал', 'Плейт', 'сильная'),
    ('Сенегал', 'Палмейрас', 'слабая'), ('Бразилия', 'Плейт', 'сильная'),
    ('США', 'Наполи', 'средняя'), ('Канада', 'Боруссия', 'слабая'),
    ('Бельгия', 'Сити', 'слабая'), ('Швеция', 'Барселона', 'средняя')]
print(TEAMS)


def generate_test_data() -> None:
    if not cursor.execute("SELECT EXISTS (SELECT * FROM uefa_commands)"):
        print("Выполнение кода")
        cursor.executemany(
            f"INSERT INTO uefa_commands (command_country, command_name, command_level) VALUES (?, ?, ?)",
            TEAMS
        )
    else:
        print("Выполняется жеребьевка")
        cursor.execute("DELETE FROM uefa_draw")

        for number in range(1, number_of_groups + 1):
            groups = []
            for i in range(3):
                response = cursor.execute(f"SELECT command_number FROM uefa_commands WHERE command_level = '{LEVEL_TEAM[i]}'")
                com_num = response.fetchall()
                if i == 1:
                    new_tuple = (number,)
                    new_tuple = new_tuple + random.choice(com_num)
                    groups.append(new_tuple)
                new_tuple = (number,)
                new_tuple = new_tuple + random.choice(com_num)
                groups.append(new_tuple)
            cursor.executemany(
                f"INSERT INTO uefa_draw (group_number, command_number) VALUES (?, ?)", groups)


if __name__ == '__main__':
    number_of_groups: int = int(input('Введите количество групп (от 4 до 16): '))
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        generate_test_data()
        conn.commit()
