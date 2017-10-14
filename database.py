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


def add_new_activity(title, full_message, author, author_name):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        'insert into entries (title, full_message, author, author_name) values (?, ?, ?, ?)', 
        (title, full_message, author, author_name))
    db.commit()
    return cursor.lastrowid


def update_activity(activity_id, chat_id, message_id):
    db = get_db()
    db.execute(
        'update entries set chat_id = ?, message_id = ? where id = ?', 
        (chat_id, message_id, activity_id))
    db.commit()


def get_activities():
    db = get_db()
    cur = db.execute('select * from entries order by id asc')
    entries = cur.fetchall()
    return [dict(x) for x in entries]


def get_activity_by_id(activity_id):
    db = get_db()
    cur = db.execute('select * from entries where id = ?', (activity_id, ))
    entries = cur.fetchall()
    return [dict(x) for x in entries][0]


def get_activity_by_msg(chat_id, message_id):
    db = get_db()
    cur = db.execute('select * from entries where chat_id = ? and message_id = ?', (chat_id, message_id))
    entries = cur.fetchall()
    return [dict(x) for x in entries][0]


def get_likes(activity_id):
    db = get_db()
    cur = db.execute('select distinct person, person_name from likes where id = (?)', (int(activity_id), ))
    entries = cur.fetchall()
    return [dict(x) for x in entries]


def add_like(activity_id, user_id, user_name):
    # TODO: check if like exists
    db = get_db()
    db.execute('insert into likes (id, person, person_name) values (?, ?, ?)', (activity_id, user_id, user_name))
    db.commit()


def remove_like(activity_id, user_id):
    db = get_db()
    db.execute('delete from likes where id = ? and person = ?', (activity_id, user_id))
    db.commit()


def get_dislikes(activity_id):
    db = get_db()
    cur = db.execute('select distinct person, person_name from dislikes where id = (?)', (int(activity_id), ))
    entries = cur.fetchall()
    return [dict(x) for x in entries]


def add_dislike(activity_id, user_id, user_name):
    # TODO: check if like exists
    db = get_db()
    db.execute('insert into dislikes (id, person, person_name) values (?, ?, ?)', (activity_id, user_id, user_name))
    db.commit()


def remove_dislike(activity_id, user_id):
    db = get_db()
    db.execute('delete from dislikes where id = ? and person = ?', (activity_id, user_id))
    db.commit()


if __name__ == '__main__':
    init_db()
    print('Initialized the database.')
