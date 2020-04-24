from flask import render_template, flash, redirect, url_for, jsonify, request, make_response
import random

import db
from app import app
from app.forms import JoinGameForm, AddNewCategoryForm


@app.route('/')
@app.route('/index')
def index():
    form = AddNewCategoryForm()
    return render_template("index.html", form=form)


@app.route('/login')
def login():
    form = JoinGameForm()
    return render_template("login.html", form=form)


@app.route("/gen_session_code")
def gen_session_code():
    while True:
        session_code = "%s %s" % (random.randint(100, 1000), random.randint(100, 1000))
        if not db.get_session(session_code):
            break
    db.create_session(session_code)
    return jsonify({"game_code": session_code})


@app.route("/join_game", methods=['POST'])
def join_game():
    session_code = request.form["session_code"]
    player_name = request.form["player"]
    if not db.get_session(session_code):
        flash("No game session found")
        return redirect(url_for('login'))
    if db.get_player(session_code, player_name):
        flash("Player %s already exists" % player_name)
        return redirect(url_for('login'))

    db.create_player(session_code, player_name)

    response = make_response(redirect(url_for('play_game')))
    response.set_cookie('player', player_name)
    response.set_cookie('session_code', session_code)
    return response


@app.route('/add_category', methods=['POST'])
def add_category():
    category = request.form["category"]
    db.add_category(category)
    return jsonify({'success': True})


@app.route('/gen_categories')
def gen_categories():
    session_code = request.cookies.get('session_code')
    categories = db.get_twelve_categories()
    db.insert_session_categories(session_code, categories)
    db.update_round(session_code)
    return jsonify({'categories': categories})


@app.route('/get_categories')
def get_categories():
    session_code = request.cookies.get('session_code')
    game_data = db.get_session_categories(session_code)
    game_round = game_data["round"]
    try:
        categories = game_data["categories"][0]
    except KeyError:
        # Categories haven't been created yet
        return jsonify({"info": "categories not yet created"})
    return jsonify({"round": game_round, "categories": categories})


@app.route('/play')
def play_game():
    return render_template("play.html")
