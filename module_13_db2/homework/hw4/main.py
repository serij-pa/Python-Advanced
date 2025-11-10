import sqlite3
SALARY_SOVIN = 100000


def ivan_sovin_the_most_effective(
        cursor_sovin: sqlite3.Cursor,
        name_employee: str,
) -> None:
    resp = cursor_sovin.execute(f"SELECT salary FROM table_effective_manager WHERE name = '{name_employee}'")
    salary_employee = resp.fetchone()[0]
    new_salary_employee = salary_employee + (salary_employee / 10)
    print(f"З.п сотрудника {name_employee} после увеличение составит: {new_salary_employee}")
    if new_salary_employee < SALARY_SOVIN:
        cursor_sovin.execute(f"UPDATE table_effective_manager SET salary = {int(new_salary_employee)} WHERE name = '{name_employee}'")
        print("Новая зар.плата внесена в базу")

    else:
        cursor.execute(f"DELETE FROM table_effective_manager"
                       f"WHERE name='{name_employee}'")
        print(f"Сотрудник {name_employee} уволен")
    ...


if __name__ == '__main__':
    name: str = input('Введите имя сотрудника: ')
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        ivan_sovin_the_most_effective(cursor, name)
        conn.commit()
