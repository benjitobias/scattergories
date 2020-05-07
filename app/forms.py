from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired

from config import *


class AddNewWordForm(FlaskForm):
    word = StringField('Word', validators=[DataRequired()], id="new_word")
    submit = SubmitField("Add")


class AddNewCategoryForm(FlaskForm):
    category = StringField('Category', validators=[DataRequired()], id="new_category")
    submit = SubmitField("Add")


class UpdateCategoryForm(FlaskForm):
    category = StringField('Category', id="category")
    category_id = HiddenField()


class DeleteCategoryForm(FlaskForm):
    category_id = HiddenField()


class JoinGameForm(FlaskForm):
    # player = StringField('Player name', validators=[DataRequired()], id="player")
    session_code = StringField('Game code', validators=[DataRequired()], id="session_code")
    submit = SubmitField("Join!")
