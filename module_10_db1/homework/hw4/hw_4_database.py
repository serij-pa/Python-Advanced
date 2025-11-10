import sqlite3

if __name__ == "__main__":
    with sqlite3.connect("hw_4_database.db") as conn:
        cursor = conn.cursor()

        print(f"1. Выяснить, сколько человек с острова N получает меньше 5000 гульденов в год.")
        quantity = cursor.execute(f"SELECT COUNT(*) FROM salaries WHERE salaries.salary < 5000")
        result1 = quantity.fetchall()[0][0]
        print(f"\t{result1} человек с острова N получает меньше 5000 гульденов в год")

        print(f"2. Посчитать среднюю зарплату по острову N.")
        average = cursor.execute(f"SELECT ROUND(AVG(salary), 2) FROM salaries")
        result2 = average.fetchall()[0][0]
        print(f"\tСредняя зарплата по острову N составляет {result2}")

        print(f"3. Посчитать медианную зарплату по острову.")
        median_salary = cursor.execute("""SELECT salary FROM (SELECT ROW_NUMBER () OVER (ORDER BY salary) RN, salary FROM salaries) WHERE RN = (SELECT COUNT(*) / 2 + 1 FROM salaries)""")
        result3 = median_salary.fetchall()[0][0]
        print(f"\tМедианная зарплата по острову {result3}")

        print(f"4. Посчитать число социального неравенства")
        social_inequality = cursor.execute("""SELECT ROUND(SUM(salary)* 1.0 / (SELECT SUM(salary) - (SELECT SUM(salary) FROM (SELECT * FROM salaries ORDER BY salary DESC LIMIT 0.1 * (SELECT COUNT(*) FROM salaries))) FROM salaries) * 1.0, 2) FROM (SELECT * FROM salaries ORDER BY salary DESC LIMIT 0.1 * (SELECT COUNT(*) FROM salaries))""")
        result4 = social_inequality.fetchall()[0][0]
        print(f"\tЧисло социального неравенства {result4}")





