import sqlite3


def check_if_vaccine_has_spoiled(
        cursor: sqlite3.Cursor,
        tru_number: str
) -> bool:
    resp = cursor.execute(f"""
        SELECT EXISTS (SELECT * FROM table_truck_with_vaccine WHERE truck_number='{tru_number}'
        AND temperature_in_celsius NOT BETWEEN 16 AND 20)
    """)
    result = resp.fetchone()[0]
    return result


if __name__ == '__main__':
    truck_number: str = input('Введите номер грузовика: ')
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        spoiled: bool = check_if_vaccine_has_spoiled(cursor, truck_number)
        print('Испортилась' if spoiled else 'Не испортилась')
        conn.commit()
