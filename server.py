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
    activity_id = request.args.get('activity_id')
    return json.dumps(database.get_likes(activity_id), ensure_ascii=False, indent=4)

@app.route('/add_like', methods=['GET'])
def add_like():
    activity_id = request.args.get('activity_id')
    user_id = request.args.get('user_id')
    database.add_like(activity_id, user_id)

@app.route('/remove_like', methods=['GET'])
def remove_like():
    activity_id = request.args.get('activity_id')
    user_id = request.args.get('user_id')
    database.remove_like(activity_id, user_id)
