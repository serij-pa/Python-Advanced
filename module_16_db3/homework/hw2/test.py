import sqlite3


sqk_request_1 = """
SELECT cust.full_name, man.full_name, purchase_amount, date FROM 'order'
INNER JOIN customer cust ON cust.customer_id = 'order'.customer_id
INNER JOIN manager man ON man.manager_id = 'order'.manager_id
"""

sqk_request_2 = """
SELECT cust.full_name FROM customer as cust
LEFT JOIN 'order' ord ON cust.customer_id = ord.customer_id
WHERE ord.customer_id IS NULL ORDER BY full_name
"""

sqk_request_3 = """
SELECT order_no, man.full_name, cust.full_name FROM 'order'
INNER JOIN customer cust ON cust.customer_id = 'order'.customer_id
INNER JOIN manager man ON man.manager_id = 'order'.manager_id
WHERE man.city != cust.city
"""

sqk_request_4 = """
SELECT order_no, cust.full_name FROM 'order'
INNER JOIN customer cust ON cust.customer_id = 'order'.customer_id
WHERE 'order'.manager_id IS NULL
"""

sqk_request_5 = """
SELECT city, full_name, manager_id FROM customer
WHERE customer_id < 9
ORDER BY manager_id
"""

def create_db():
    with sqlite3.connect('../hw.db') as conn:
        cursor = conn.cursor()
        result = cursor.execute(sqk_request_2).fetchall()
        for res in result:
            print(res)

if __name__ == '__main__':
    create_db()