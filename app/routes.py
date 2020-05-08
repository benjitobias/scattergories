from flask import render_template, flash, redirect, url_for, jsonify, request, make_response
import random
import string
from urllib.parse import quote
import db
from app import app
from app.forms import JoinGameForm, AddNewCategoryForm, UpdateCategoryForm, DeleteCategoryForm


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
    if " " not in session_code:
        session_code = session_code[:3] + " " + session_code[3:]
#    player_name = request.form["player"]
    if not db.get_session(session_code):
        flash("No game session found")
        return redirect(url_for('login'))
#    if db.get_player(session_code, player_name):
#        flash("Player %s already exists" % player_name)
#        return redirect(url_for('login'))

#    db.create_player(session_code, player_name)

    response = make_response(redirect(url_for('play_game')))
#    response.set_cookie('player', player_name)
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
    letter = random.choice(string.ascii_uppercase.replace("X", ""))
    db.insert_session_letter(session_code, letter)
    db.update_round(session_code)

    return jsonify({'categories': categories})


@app.route('/get_categories')
def get_categories():
    session_code = request.cookies.get('session_code')
    game_data = db.get_session_categories(session_code)
    game_round = game_data["round"]
    try:
        letter = db.get_session_letter(session_code)["letter"]
        categories = game_data["categories"][0]
    except KeyError:
        # Categories haven't been created yet
        return jsonify({"info": "categories not yet created"})
    return jsonify({"round": game_round, "categories": categories, "letter": letter})


@app.route('/play', methods=['GET'])
def play_game():
    session_code = None
    session_param = request.args.get("session_code")
    session_cookie = request.cookies.get('session_code')
    host_cookie = request.cookies.get('host')
    if session_param:
        session_code = session_param
    else:
        session_code = session_cookie
    if not session_code:
        flash("First join a game!")
        return redirect(url_for('login'))
    if not db.get_session(session_code):
        flash("No game session found")
        return redirect(url_for('login'))
    print(session_code)
    share_link = request.url_root + url_for("play_game") + "?session_code=" + quote(session_code)
    if host_cookie == session_code:
        host = True
    else:
        host = False
    response = make_response(render_template("play.html", session_code=session_code, host=host, share_link=share_link))
    if not session_cookie:
        response.set_cookie('session_code', session_param)
    return response


@app.route('/manage_categories')
def manage_categories():
    categories = db.get_all_categories()
    add_form = AddNewCategoryForm()
    update_form = UpdateCategoryForm()
    delete_form = DeleteCategoryForm()
    return render_template("categories.html", categories=categories,
                           add_form=add_form, update_form=update_form, delete_form=delete_form)


@app.route('/update_category', methods=['POST'])
def update_category():
    category_id = request.form["category_id"]
    new_category = request.form["category"]
    db.update_category(category_id, new_category)
    return jsonify({'category': new_category, "_id": category_id})


@app.route('/delete_category', methods=['POST'])
def delete_category():
    category_id = request.form["category_id"]
    db.delete_category(category_id)
    return jsonify({"_id": category_id})
