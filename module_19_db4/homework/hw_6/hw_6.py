#Используя подзапросы, выведите среднюю оценку за те задания,
# где ученикам нужно было что-то прочитать и выучить.

import sqlite3

SELECTION_1 = """select a.assisgnment_id from assignments a
            WHERE a.assignment_text LIKE '%прочитать%' OR a.assignment_text LIKE '%выучить%'"""

SELECTION_2 = f"""select ag.assisgnment_id, ROUND(AVG(ag.grade), 2) as "Ср.оценка за почитать или выучить"
            from assignments_grades ag WHERE ag.assisgnment_id in
            ({SELECTION_1})
            GROUP BY ag.assisgnment_id"""

SELECTION_3 = """select ag.assisgnment_id, ROUND(AVG(ag.grade), 2) as "Ср.оценка за почитать или выучить"
            from assignments_grades ag WHERE ag.assisgnment_id in
            (select a.assisgnment_id from assignments a
            WHERE a.assignment_text LIKE "%прочитать%" OR a.assignment_text LIKE "%выучить%")
            GROUP BY ag.assisgnment_id"""

if __name__ == "__main__":
    with sqlite3.connect("../../homework.db") as conn:
        cursor = conn.cursor()
        #cursor.execute("SELECT * FROM students WHERE group_id = 1")
        cursor.execute(SELECTION_2)
        users = cursor.fetchall()
        print(users)
        for user in users:
            print(user)