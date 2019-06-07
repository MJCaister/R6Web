from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class SubmitData(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    kills = IntegerField('Kills', validators=[DataRequired()])
    deaths = IntegerField('Deaths', validators=[DataRequired()])
    MMR = IntegerField('MMR/ELO after game', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class Signup(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    # image = 
    submit = SubmitField('Sign Up')


class UserSearch(FlaskForm):
    username_search = StringField('Search for a player',
                                  validators=[DataRequired()])
    submit = SubmitField('Search')
