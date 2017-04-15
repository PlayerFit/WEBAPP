from flask import Flask, redirect, url_for, request, render_template
from models import Prospect
from database import db_session
from twitter import add_prospect

app = Flask(__name__)

@app.route('/')
def home():
    #TODO: Render homepage HTML
    return render_template('home.html')

@app.route('/prospect', methods=['POST', 'GET'])
def prospect():
    #TODO: render a list of all players with data available
    if request.method == 'POST':
        #TODO: switch to Redis Queue for data fetching jobs
        prospect_handle = request.form["handle"]
        add_prospect(prospect_handle)
        return redirect(url_for('prospect'))
    elif request.method == 'GET':
        prospect_list = Prospect.query.all()
        return render_template("prospects.html", items=prospect_list)
    else:
        return redirect(url_for('/'))

@app.route('/prospect/<int:prospect_id>')
def prospect_one(prospect_id):
    #TODO: show all of the widgets for the player with player_id
    return 'Prospect %d' % prospect_id

# Initialize Database
from database import init_db
init_db()
