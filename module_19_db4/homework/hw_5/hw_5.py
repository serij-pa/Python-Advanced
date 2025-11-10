#Проанализируйте все группы по следующим критериям:
# общее количество учеников,
# средняя оценка,
# количество учеников,
#   которые не сдали работы,
#   которые просрочили дедлайн,
#   количество повторных попыток сдать работу.


import sqlite3

SELECTION_1 = """select s.group_id, count(s.group_id) 
                    from students s 
                    group by s.group_id"""

SELECTION_2 = """select s.group_id, round(AVG(ag.grade), 2)
                    from students s
                    join assignments_grades ag 
                    on s.student_id = ag.student_id
                    group by s.group_id"""

SELECTION_3 = """select count(s.student_id) as 'не сдали работы'
                    from assignments_grades ag
                    right join students s
                    on s.student_id = ag.student_id
                    where ag.grade_id is NULL"""

SELECTION_4 = """select count(ag.student_id) as 'просрочили дедлайн'
                    from students_groups sg
                    join assignments a on sg.group_id = a.group_id
                    join assignments_grades ag on a.assisgnment_id = ag.assisgnment_id
                    where ag.date > a.due_date
                    """

SELECTION_5 = """select count(student_id) as 'повторных попыток'
                    from (select student_id, count(1)
                            from assignments_grades ag
                            group by student_id
                            having count(1) > 1
                        )
                    """

if __name__ == "__main__":
    with sqlite3.connect("../../homework.db") as conn:
        cursor = conn.cursor()
        #cursor.execute("SELECT * FROM students WHERE group_id = 1")
        cursor.execute(SELECTION_1)
        select_1 = cursor.fetchall()
        print("\nОбщее количество учеников")
        for sel1 in select_1:
            print(f"Группа: {sel1[0]}, учеников: {sel1[1]}")

        cursor.execute(SELECTION_2)
        select_2 = cursor.fetchall()
        print("\nCредняя оценка")
        for sel2 in select_2:
            print(f"Группа: {sel2[0]}, средняя оценка: {sel2[1]}")

        cursor.execute(SELECTION_3)
        select_3 = cursor.fetchone()
        print(f"\nКоличество учеников которые не сдали работы: {select_3[0]}")

        cursor.execute(SELECTION_4)
        select_4 = cursor.fetchone()
        print(f"Количество учеников которые просрочили дедлайн: {select_4[0]}")

        cursor.execute(SELECTION_5)
        select_5 = cursor.fetchone()
        print(f"Количество повторных попыток сдать работу: {select_5[0]}")