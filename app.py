from flask import Flask, redirect, url_for, request, render_template
from models import Prospect
from database import db_session

app = Flask(__name__)

@app.route('/')
def home():
    #TODO: Render homepage HTML
    return render_template('home.html')

@app.route('/player/new', methods=['POST'])
def get_new_player_data():
    if request.method == 'POST':
        #TODO: tell backend to start fetching the data
        return 'Fetching data'
    else:
        redirect(url_for('/'))

@app.route('/player')
def players():
    #TODO: render a list of all players with data available
    return 'List of players here'

@app.route('/player/<int:player_id>')
def player(player_id):
    #TODO: show all of the widgets for the player with player_id
    return 'Player %d' % player_id

# Initialize Database
from database import init_db
init_db()
