from flask import Flask, redirect, url_for, request, render_template
from celery import Celery
from models import Prospect, Tweet
from database import db_session
from twitter import add_prospect

import helpers as h

app = Flask(__name__)
celery = Celery(app.name, broker='redis://localhost:6379', backend='redis://localhost:6379')

@celery.task
def add_together(a,b):
    return a + b

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/prospect', methods=['POST', 'GET'])
def prospect():
    if request.method == 'POST':
        #TODO: switch to Redis Queue for data fetching jobs
        prospect_handle = request.form["handle"]
        result = add_together.delay(10,10).wait()
        print result
        add_prospect(prospect_handle)
        return redirect(url_for('prospect'))
    elif request.method == 'GET':
        prospect_list = Prospect.query.all()
        return render_template("prospects.html", items=prospect_list)
    else:
        return redirect(url_for('/'))

@app.route('/prospect/<int:prospect_id>')
def prospect_one(prospect_id):
    pid = str(prospect_id)
    prospect = Prospect.query.filter_by(id=pid).one()
    tweets_by_hour = h.get_tweets_by_hour(pid)
    top_hashtags = h.get_most_common_hashtags(pid)
    top_user_mentions = h.get_most_common_handles(pid)
    top_locations = h.get_most_common_locations(pid)
    return render_template('prospect.html', prospect=prospect, tweets_by_hour=tweets_by_hour, hashtags=top_hashtags,
        user_mentions=top_user_mentions, locations=top_locations)

# Initialize Database
from database import init_db
init_db()
