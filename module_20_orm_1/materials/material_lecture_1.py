from sqlalchemy import create_engine, text

if __name__ == '__main__':

    engine = create_engine("sqlite:///python.db")
    with engine.connect() as conn:

        create_user_table = """CREATE TABLE IF NOT EXISTS users 
                                (id integer PRIMARY KEY, name text)"""
        conn.execute(create_user_table)

        insert_q = """INSERT INTO users(name) VALUES ('SERGEY')"""
        conn.execute(insert_q)
        filter_query = text("SELECT * FROM users WHERE id=:user_id")
        cursor = conn.execute(filter_query, user_id=1)
        result = cursor.fetchone()
        print(result)