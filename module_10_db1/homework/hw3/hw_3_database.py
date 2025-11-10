import sqlite3

if __name__ == "__main__":
    with sqlite3.connect("hw_3_database.db") as conn:
        cursor = conn.cursor()

        print(f"\n1. Сколько записей (строк) хранится в каждой таблице?")
        for num in range(1, 4):
            quantity_rows = cursor.execute(f"SELECT COUNT(*) FROM table_{num}")
            result1 = quantity_rows.fetchall()[0][0]
            print(f"\t В {num} таблице {result1} строк")

        print(f"\n2. Сколько в таблице table_1 уникальных записей?\n"
              f"Назовём уникальной такую запись, которая ранее не встречалась в таблице.")
        uniq_rows = cursor.execute(f"SELECT COUNT(DISTINCT id) FROM table_1")
        result2 = uniq_rows.fetchall()[0][0]
        print(f"\t{result2} уникальных записей в таблице_1")

        print(f"\n3. Как много записей из таблицы table_1 встречается в table_2?")
        coincidences_1_2 = cursor.execute(f"SELECT COUNT(*) FROM table_1 JOIN table_2  USING (id)") # table_1.id = table_2.id
        result3 = coincidences_1_2.fetchall()[0][0]
        print(f"\t{result3} записей таблицы table_1 встречается в table_2")


        print(f"\n4. Как много записей из таблицы table_1 встречается и в table_2, и в table_3?")
        coincidences_1_2_3 = cursor.execute(f"SELECT COUNT(*) FROM table_1 JOIN table_2 USING (id) JOIN table_3 USING (id)") # table_1.id = table_2.id
        result3 = coincidences_1_2_3.fetchall()[0][0]
        print(f"\t{result3} записей таблицы table_1 встречается и в table_2 и в table_3")

