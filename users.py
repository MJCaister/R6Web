from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, ValidationError


class SubmitData(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    kills = IntegerField('Kills', validators=[DataRequired("Please enter a number")])
    deaths = IntegerField('Deaths', validators=[DataRequired("Please enter a number")])
    MMR = IntegerField('MMR/ELO after game', validators=[DataRequired("Please enter a number")])
    submit = SubmitField('Sign In')


class Signup(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    image = FileField('Profile Image (This can be added later)', validators=[
    FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('Sign Up')


class UserSearch(FlaskForm):
    username_search = StringField('Search for a player',
                                  validators=[DataRequired()])
    submit = SubmitField('Search')
