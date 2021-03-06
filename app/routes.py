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

    #response = make_response(render_template())
    return session_code + " - " + player_name


@app.route('/add_category', methods=['POST'])
def add_category():
    category = request.form["category"]
    db.add_category(category)
    return jsonify({'success': True})


@app.route('/get_categories')
def get_categories():
    categories = db.get_twelve_categories()
    return jsonify({'categories': categories})
