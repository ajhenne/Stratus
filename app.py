from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_login import LoginManager, login_required, login_user, logout_user, current_user, UserMixin, AnonymousUserMixin

from sqlalchemy import create_engine, Table, MetaData, text, insert
from sqlalchemy.orm import sessionmaker
from classes import Pokemon, Aprimon

from werkzeug.security import check_password_hash, generate_password_hash

import json
import os

# Create tables.
engine = create_engine('sqlite:///database.db')
meta = MetaData()
meta.create_all(engine)
table_aprimon = Table('aprimon_master', meta, autoload_with=engine)
 
Session = sessionmaker(bind=engine)
session = Session()

class User(UserMixin):
    def __init__(self, name, id, active=True):
        self.name = name
        self.id = id
        self.active = active

    def is_active(self):
        return self.active

USERS = {
    1: User(u"henne", 1)
}

USER_NAMES = dict((u[1].name, u[1]) for u in USERS.items())

app = Flask(__name__, template_folder='pages')
app.config['SECRET_KEY'] = 'stratus2023'
app.config.from_object(__name__)

admin_hashed_pass = os.getenv('STRATUS_KEY')

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message = u"Please log in to access this page."
login_manager.refresh_view = "reauth"

@login_manager.user_loader
def load_user(id):
    return USERS.get(int(id))

login_manager.init_app(app)

apriballNames = ('fast', 'lure', 'level', 'heavy', 'love', 'moon', 'dream', 'safari', 'beast', 'sport')

### HOME PAGE ######################################################################


@app.template_filter('dexformat')
def dexformat(value):
    return f"{value:04}"

@app.route('/')
def index():
    # Check logged in.
    if current_user.is_authenticated:
        check_login_status = True
    else:
        check_login_status = False

    return render_template("index.html", title='ApriScout')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = 'henne'
        password = request.json.get('password')

        if check_password_hash(admin_hashed_pass, password):
            login_user(USER_NAMES[username], remember=False)
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'invalid_pass', 'message': 'Wrong password. Please try again.'})

@app.route("/logout")
@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for('aprimon'))
    else:
        return jsonify({'status': 'error'})

### MASTER APRIMON TABLE ###########################################################

@app.route('/aprimon')
def aprimon():
    # Get data from table.
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM aprimon_master"))
        rows = result.fetchall()
        conn.close()
        columns = result.keys()
        row_data = [dict(zip(columns, row)) for row in rows]
    # Check logged in.
    if current_user.is_authenticated:
        check_login_status = True
    else:
        check_login_status = False
    return render_template('aprimon.html', data=row_data, login_status=check_login_status, ball_list=apriballNames)

@app.route('/add_aprimon', methods=['POST'])
@login_required
def add_row():
    name_id = int(request.json.get('selectedPokemon'))
    add_pokemon = {ballname: value for ballname, value in zip(apriballNames, request.json.get('apriballTypes'))}
    add_pokemon['internalId'] = name_id

    try:
        with engine.connect() as conn:

            # Check if this entry is already in Aprimon table.
            already_exists = session.query(Aprimon).filter(Aprimon.internalId == name_id).first()
            if already_exists:
                return jsonify({'status': 'already_exists'})
            
            # Get information data from Pokemon talb.e
            pokemon_data = session.query(Pokemon).filter(Pokemon.internalId == name_id).first()
            if pokemon_data:
                add_pokemon['name'] = pokemon_data.name
                add_pokemon['dexnum'] = pokemon_data.dexNum
                add_pokemon['sprite'] = pokemon_data.sprite
            else:
                return jsonify({'status': 'pokemon_not_found'})
            
            addrow = insert(table_aprimon).values(**add_pokemon)
            conn.execute(addrow)
            conn.commit()
            conn.close()
        return jsonify({'status': 'success'})
    
    except Exception:
        return jsonify({'error': 'An error occured whilst processing the request'}), 500

@app.route('/update_apriballs', methods=['POST'])
@login_required
def update_balls():

    try:
        data = request.get_json()

        if len(data) == 0:
            return jsonify({'status': 'success', 'message': 'No data updated, returning.'}), 500
        
        for change in data:
            session.query(Aprimon).filter(Aprimon.internalId == change['internalId']).update({change['selected_ball']: change['selected']})
            session.commit()

        return jsonify({'status': 'success', 'message': f'Sucessfully updated {len(data)} records.'}), 200
    
    except Exception:
        return jsonify({'error': 'An error occured whilst processing the request'}), 500

@app.route('/search_pokemon', methods=['POST'])
@login_required
def search_pokemon():
    search = request.json.get('name')
    if search:
        with engine.connect() as conn:
            matching_pokemon = session.query(Pokemon).filter(Pokemon.name.like(f"{search}%")).all()
            results = [{'internalId': pokemon.internalId, 'name': pokemon.name, 'sprite': pokemon.sprite} for pokemon in matching_pokemon]

            if len(matching_pokemon) > 0:
                return jsonify({'status': 'success', 'results': results})

            return jsonify({'status': 'not_found'})
    
    return jsonify({'status': 'error'})

####################################################################################

if __name__ == '__main__':

    # app.run()
    app.run(debug=True)
