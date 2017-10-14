import sqlite3
import os

DATABASE = 'flaskr.db'


def connect_db():
    rv = sqlite3.connect(DATABASE, check_same_thread=False)
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
    db = get_db()
    db.execute('insert into entries (title, author) values (?, ?)', (title, author))
    db.commit()
    return db.lastrowid


def get_activities():
    db = get_db()
    cur = db.execute('select id, title, author from entries order by id asc')
    entries = cur.fetchall()
    return [dict(x) for x in entries]


def get_likes(activity_id):
    db = get_db()
    cur = db.execute('select distinct person from likes where id == (?)', (int(activity_id), ))
    entries = cur.fetchall()
    return [dict(x) for x in entries]


def add_like(activity_id, user_id):
    # TODO: check if like exists
    print(322, activity_id, user_id)
    db = get_db()
    db.execute('insert into likes (id, person) values (?, ?)', (activity_id, user_id))
    db.commit()
