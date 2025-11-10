#Используя вложенные запросы, найдите всех учеников того преподавателя,
# который задаёт самые простые задания, то есть те задания, за которые
# ученики получают самый высокий средний балл.

import sqlite3

SELECTION_1 = """SELECT a.teacher_id, ag.assisgnment_id, AVG(ag.grade) as avg_score
                FROM assignments_grades ag
                JOIN assignments a ON ag.assisgnment_id = a.assisgnment_id
                GROUP BY ag.assisgnment_id 
                ORDER BY avg_score DESC"""

SELECTION_2 = f"""SELECT teacher_id, assisgnment_id, max(avg_score) as max_score FROM ({SELECTION_1})"""

SELECTION_3 = f"""SELECT teacher_id FROM ({SELECTION_2})"""

SELECTION_4 = f"""SELECT group_id FROM students_groups sg WHERE teacher_id =({SELECTION_3})"""

SELECTION_5 = f"""SELECT full_name FROM students s WHERE group_id IN ({SELECTION_4})"""

SELECTION_6 = """
            SELECT full_name FROM students s WHERE group_id IN (
                SELECT group_id FROM students_groups sg WHERE teacher_id =(
                    SELECT teacher_id FROM (
                        SELECT teacher_id, assisgnment_id, max(avg_score) as max_score FROM (
                            SELECT a.teacher_id, ag.assisgnment_id, AVG(ag.grade) as avg_score
                            FROM assignments_grades ag
                            JOIN assignments a ON ag.assisgnment_id = a.assisgnment_id
                            GROUP BY ag.assisgnment_id ORDER BY avg_score DESC
            ))))

        """

if __name__ == "__main__":
    with sqlite3.connect("../../homework.db") as conn:
        cursor = conn.cursor()
        #cursor.execute("SELECT * FROM students WHERE group_id = 1")
        cursor.execute(SELECTION_5)
        users = cursor.fetchall()
        print(users)
        for user in users:
            print(user)