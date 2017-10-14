import sqlite3
import os

DATABASE = 'flaskr.db'


def connect_db():
    rv = sqlite3.connect(DATABASE)
    rv.row_factory = sqlite3.Row
    return rv


sqlite_db = None

def get_db():
    global sqlite_db
    if sqlite_db is None:
        sqlite_db = connect_db()
    return sqlite_db


def init_db():
    db = get_db()
    with open('schema.sql', 'r') as f:
        db.cursor().executescript(f.read())
    db.commit()


def close_db(error):
    global sqlite_db
    if sqlite_db is not None:
        sqlite_db.close()
        sqlite_db = None


def add_new_activity(title, author):
    db = database.get_db()
    db.execute('insert into entries (title, author) values (?, ?)', (title, author))
    db.commit()
