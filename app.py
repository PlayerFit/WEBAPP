import os
import time
from rq import Queue
from rq.job import Job
from worker import conn
from flask import Flask, redirect, url_for, request, jsonify, render_template, session, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, login_user, logout_user

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

q = Queue(connection=conn)

import helpers as h
from tasks import add_prospect, get_tweets
from models import *

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

####################################
#### LOGIN/LOGOUT/SIGNUP ROUTES ####
####################################
@app.route("/signup", methods=["POST"])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_confirmation = request.form['password_confirmation']
        if username is None or password is None or password_confirmation is None:
            abort(400)    # missing arguments
        if password != password_confirmation:
            abort(400)
        if User.query.filter_by(username=username).first() is not None:
            abort(400)    # existing user
        user = User(username=username)
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

# somewhere to login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user is None:
            abort(400) # Unknown username
        if not user.verify_password(password):
            abort(400) # Wrong password
        login_user(user)
        return redirect(url_for('prospect'))
    else:
        return render_template("login.html")

# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

# callback to reload the user object
@login_manager.user_loader
def load_user(userid):
    user = User.query.filter_by(id=userid).first()
    return user
############################


###############################
#### ROUTES FOR MAIN VIEWS ####
###############################
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/prospect', methods=['POST', 'GET'])
@login_required
def prospect():
    if request.method == 'POST':
        prospect_handle = request.form["handle"]
        job = q.enqueue(add_prospect, prospect_handle)
        time.sleep(3)
        q.enqueue(get_tweets, job.result, depends_on=job, timeout=600)
        return redirect(url_for('prospect'))
    elif request.method == 'GET':
        processed = Prospect.query.with_entities(Prospect.id, Prospect.img_url, Prospect.name).filter_by(has_tweets=True).all()
        processing = Prospect.query.with_entities(Prospect.id, Prospect.img_url, Prospect.name).filter_by(has_tweets=False).all()
        return render_template("prospects.html", processed=processed, processing=processing)
    else:
        return redirect(url_for('home'))

@app.route('/prospect/<int:prospect_id>')
@login_required
def prospect_one(prospect_id):
    pid = str(prospect_id)
    prospect = Prospect.query.filter_by(id=pid).one()
    tweets_by_hour = h.get_tweets_by_hour(pid)
    top_hashtags = h.get_most_common_hashtags(pid)
    top_user_mentions = h.get_most_common_handles(pid)
    top_locations = h.get_most_common_locations(pid)
    images = h.get_image_urls(pid)
    return render_template('prospect.html', prospect=prospect, tweets_by_hour=tweets_by_hour, hashtags=top_hashtags,
        user_mentions=top_user_mentions, locations=top_locations, images=images)
###############################

if __name__ == '__main__':
    app.run()
