#Узнайте, кто из преподавателей задаёт самые сложные задания.
# Другими словами, задания какого преподавателя получают в среднем худшие оценки.

import sqlite3

SELECTION_1 = """SELECT ROUND(AVG(ag.grade), 2) as "Средняя оценка", t.full_name as "ФИО учителя" 
                FROM assignments_grades ag
                JOIN assignments a ON a.assisgnment_id = ag.assisgnment_id
                JOIN teachers t ON t.teacher_id = a.teacher_id
                GROUP BY ag.assisgnment_id"""

SELECTION_2 = f"""SELECT MIN("Средняя оценка"), "ФИО учителя" FROM ({SELECTION_1})"""

SELECTION_3 = """SELECT MIN("Средняя оценка"), "ФИО учителя" FROM (
                SELECT ROUND(AVG(ag.grade), 2) as "Средняя оценка", t.full_name as "ФИО учителя" 
                FROM assignments_grades ag
                JOIN assignments a ON a.assisgnment_id = ag.assisgnment_id
                JOIN teachers t ON t.teacher_id = a.teacher_id
                GROUP BY ag.assisgnment_id)"""

if __name__ == "__main__":
    with sqlite3.connect("../../homework.db") as conn:
        cursor = conn.cursor()
        #cursor.execute("SELECT * FROM students WHERE group_id = 1")
        cursor.execute(SELECTION_2)
        users = cursor.fetchall()
        print(users)
        for user in users:
            print(user)