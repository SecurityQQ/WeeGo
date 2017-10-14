from flask import Flask, request
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
    return json.dumps(database.get_activities(), ensure_ascii=False, indent=4)

@app.route('/get_activities', methods=['GET'])
def get_activities():
    return json.dumps(database.get_activities(), ensure_ascii=False, indent=4)

@app.route('/get_aggregated_activities', methods=['GET'])
def get_aggregated_activities():
    activities = database.get_activities()
    aggreagated_activities = {}
    for activity in activities:
        if activity['title'] not in aggreagated_activities:
            aggreagated_activities[activity['title']] = {}
        for person in database.get_likes(activity['id']):
            aggreagated_activities[activity['title']][person['person']] = person

    response = []
    for k, v in aggreagated_activities.items():
        response.append({'title': k, 'likes': list(v.values())})
    return json.dumps(response, ensure_ascii=False, indent=4)


@app.route('/add_activity', methods=['GET'])
def add_activities():
    title = request.args.get('title')
    description = request.args.get('description')
    user_id = request.args.get('user_id')
    user_name = request.args.get('user_name')
    user_username = request.args.get('user_username')
    activity_id = database.add_new_activity(title, '', '', description, user_id, user_name, user_username)
    database.add_like(activity_id, user_id, user_name, user_username)
    return json.dumps({'status': 'ok'})

@app.route('/get_likes', methods=['GET'])
def get_likes():
    activity_id = request.args.get('activity_id')
    return json.dumps(database.get_likes(activity_id), ensure_ascii=False, indent=4)

@app.route('/add_like', methods=['GET'])
def add_like():
    activity_id = request.args.get('activity_id')
    user_id = request.args.get('user_id')
    user_name = request.args.get('user_name')
    user_username = request.args.get('user_username')
    database.add_like(activity_id, user_id, user_name, user_username)
    database.remove_dislike(activity_id, user_id)
    return json.dumps({'status': 'ok'})

@app.route('/remove_like', methods=['GET'])
def remove_like():
    activity_id = request.args.get('activity_id')
    user_id = request.args.get('user_id')
    database.remove_like(activity_id, user_id)
    return json.dumps({'status': 'ok'})
