#Руководство школы решило наградить лучших учеников грамотами,
# но вот беда: картриджа в принтере хватит всего на 10 бланков.
# Выберите 10 лучших учеников с самым высоким средним баллом.
# Не забудьте отсортировать список в нисходящем порядке.

import sqlite3

SELECTION_1 = """SELECT s.full_name, AVG(ag.grade) as high_score
            FROM assignments_grades ag
            INNER JOIN students s ON s.student_id = ag.student_id
            GROUP BY ag.student_id"""

SELECTION_2 = f"""
            SELECT full_name, high_score FROM ({SELECTION_1})
            ORDER BY high_score DESC
            LIMIT 10
        """
SELECTION_3 = """
            SELECT full_name, high_score FROM (
                SELECT s.full_name, AVG(ag.grade) as high_score
                FROM assignments_grades ag
                INNER JOIN students s ON s.student_id = ag.student_id
                GROUP BY ag.student_id)
            ORDER BY high_score DESC
            LIMIT 10
        """


if __name__ == "__main__":
    with sqlite3.connect("../../homework.db") as conn:
        cursor = conn.cursor()
        #cursor.execute("SELECT * FROM students WHERE group_id = 1")
        cursor.execute(SELECTION_2)
        users = cursor.fetchall()
        print(users)
        for user in users:
            print(f"ФИО ученика: {user[0]}, баллы: {user[1]}")