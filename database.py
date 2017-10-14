import sqlite3
import os
import threading

DATABASE = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'flaskr.db')


def connect_db():
    print(DATABASE)
    rv = sqlite3.connect(DATABASE)
    rv.row_factory = sqlite3.Row
    return rv


sqlite_dbs = {}

def get_db():
    thread_id = threading.current_thread().ident
    global sqlite_dbs
    if sqlite_dbs.get(thread_id, None) is None:
        sqlite_dbs[thread_id] = connect_db()
    return sqlite_dbs[thread_id]


def init_db():
    db = get_db()
    with open('schema.sql', 'r') as f:
        db.cursor().executescript(f.read())
    db.commit()


def close_db(error):
    thread_id = threading.current_thread().ident
    global sqlite_dbs
    if sqlite_dbs.get(thread_id, None) is not None:
        sqlite_dbs[thread_id].close()
        sqlite_dbs[thread_id] = None


def add_new_activity(title, author):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('insert into entries (title, author) values (?, ?)', (title, author))
    db.commit()
    return cursor.lastrowid


def get_activities():
    db = get_db()
    cur = db.execute('select id, title, author from entries order by id asc')
    entries = cur.fetchall()
    return [dict(x) for x in entries]


def get_likes(activity_id):
    db = get_db()
    cur = db.execute('select distinct person from likes where id = (?)', (int(activity_id), ))
    entries = cur.fetchall()
    return [dict(x) for x in entries]


def add_like(activity_id, user_id):
    # TODO: check if like exists
    db = get_db()
    db.execute('insert into likes (id, person) values (?, ?)', (activity_id, user_id))
    db.commit()
