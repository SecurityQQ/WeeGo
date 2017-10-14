from flask import Flask, request, g
import os
import database
import json

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
    return json.dumps(database.get_activities())

@app.route('/get_activities', methods=['GET'])
def get_activities():
    return json.dumps(database.get_activities(), ensure_ascii=False, indent=4)

@app.route('/get_likes', methods=['GET'])
def get_likes():
    acvtivity_id = request.args.get('id')
    return json.dumps(database.get_likes(acvtivity_id), ensure_ascii=False, indent=4)
