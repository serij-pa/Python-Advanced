import sqlite3

CREATE_DATABASE = """
DROP TABLE IF EXISTS actors;
CREATE TABLE actors (
    act_id INTEGER PRIMARY KEY AUTOINCREMENT,
    act_first_name VARCHAR(255) NOT NULL,
    act_last_name VARCHAR(255) NOT NULL,
    act_gender VARCHAR(255) NOT NULL
);

DROP TABLE IF EXISTS movie;
CREATE TABLE movie (
    mov_id INTEGER PRIMARY KEY AUTOINCREMENT,
    mov_title VARCHAR(255) NOT NULL
);

DROP TABLE IF EXISTS director;
CREATE TABLE director (
    dir_id INTEGER PRIMARY KEY AUTOINCREMENT,
    dir_first_name VARCHAR(255) NOT NULL,
    dir_last_name VARCHAR(255) NOT NULL
);

DROP TABLE IF EXISTS movie_cast;
CREATE TABLE movie_cast (
    act_id INTEGER NOT NULL REFERENCES actors(act_id) ON DELETE CASCADE,
    mov_id INTEGER NOT NULL REFERENCES movie(mov_id) ON DELETE CASCADE,
    role VARCHAR(255) NOT NULL
);

DROP TABLE IF EXISTS oscar_awarded;
CREATE TABLE oscar_awarded (
    award_id INTEGER PRIMARY KEY AUTOINCREMENT,
    mov_id INTEGER NOT NULL REFERENCES movie(mov_id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS movie_direction;
CREATE TABLE movie_direction (
    dir_id INTEGER NOT NULL REFERENCES director(dir_id) ON DELETE CASCADE,
    mov_id INTEGER NOT NULL REFERENCES movie(mov_id) ON DELETE CASCADE
);
"""

with sqlite3.connect("database.db") as conn:
    cursor = conn.cursor()
    cursor.executescript(CREATE_DATABASE)
    conn.commit()