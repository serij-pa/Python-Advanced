#Используя вложенные запросы, посчитайте среднее,
# максимальное и минимальное количество просроченных
# заданий для каждого класса.

import sqlite3

SELECTION_1 = """select ag.assisgnment_id, count(ag.assisgnment_id) as 'количество просрочек', a.group_id
                    from assignments a, assignments_grades ag
                    where a.assisgnment_id = ag.assisgnment_id and (a.due_date < ag.date or ag.date is null) group by 1,3"""

SELECTION_2 = f"""select t1.group_id as 'Номер группы', 
                max(t1."количество просрочек") as 'Максимальное кол-во просрочек',
                min(t1."количество просрочек") as 'Минимальное кол-во просрочек',
                round(avg(t1."количество просрочек"),2) as 'Усредненное кол-во просрочек'
                from ({SELECTION_1}) as t1 group by 1
                """

SELECTION_3 = """select t1.group_id as 'Номер группы', 
                max(t1."количество просрочек") as 'Максимальное кол-во просрочек',
                min(t1."количество просрочек") as 'Минимальное кол-во просрочек',
                round(avg(t1."количество просрочек"),2) as 'Усредненное кол-во просрочек'
                from (
                    select ag.assisgnment_id, count(ag.assisgnment_id) as 'количество просрочек', a.group_id
                    from assignments a, assignments_grades ag
                    where a.assisgnment_id = ag.assisgnment_id and (a.due_date < ag.date or ag.date is null) group by 1,3) 
                as t1 group by 1"""

if __name__ == "__main__":
    with sqlite3.connect("../../homework.db") as conn:
        cursor = conn.cursor()
        #cursor.execute("SELECT * FROM students WHERE group_id = 1")
        cursor.execute(SELECTION_2)
        users = cursor.fetchall()
        print(users)
        for user in users:
            print(f"Группа: {user[0]}, MAX просрочек: {user[1]}, MIN просрочек: {user[2]}, Усред просрочек: {user[3]}")