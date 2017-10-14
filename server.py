from flask import Flask, request, g
import os
import database

app = Flask(__name__)
app.config.from_object(__name__) # load config from this file , flaskr.py

app.config.update(dict(
    DATABASE='flaskr.db'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    database.init_db()
    print('Initialized the database.')


@app.teardown_appcontext
def close_db(error):
    database.close_db(error)


@app.route('/')
def hello_world():
    db = database.get_db()
    cur = db.execute('select title, author from entries order by id desc')
    entries = cur.fetchall()
    return str([dict(x) for x in entries])
