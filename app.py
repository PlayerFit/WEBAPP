from flask import Flask, redirect, url_for, request, jsonify, render_template, session, abort
from flask_login import LoginManager, login_required, login_user, logout_user
from celery import Celery
from models import db, User, Prospect, Tweet
from twitter import add_prospect

import helpers as h

# SETUP APP
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
# APP SETUP

# SETUP DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://alhqpbkb:WQ-RjLbw5LrkrBMJcFKWWfbaxhsyReTs@babar.elephantsql.com:5432/alhqpbkb'
db.init_app(app)
with app.app_context():
    db.create_all()
# DB SETUP

# SETUP LOGIN
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
# LOGIN SETUP

# SETUP CELERY
celery = Celery(app.name, broker='redis://localhost:6379', backend='redis://localhost:6379')
# CELERY SETUP

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
    print user
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
        add_prospect(prospect_handle)
        return redirect(url_for('prospect'))
    elif request.method == 'GET':
        prospect_list = Prospect.query.all()
        return render_template("prospects.html", items=prospect_list)
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
