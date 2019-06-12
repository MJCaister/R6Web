from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, ValidationError


class SubmitData(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    kills = IntegerField('Kills', validators=[
                         DataRequired("Please enter a whole number.")])
    deaths = IntegerField('Deaths', validators=[
                          DataRequired("Please enter a whole number.")])
    MMR = IntegerField('MMR/ELO after game', validators=[
                       DataRequired("Please enter a whole number.")])
    submit = SubmitField('Submit Data')


class Signup(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    image = FileField('Profile Image (This can be added later) [.jpg, .png]', validators=[
                      FileAllowed(['jpg', 'png'], '.jpg or .png only!')])
    submit = SubmitField('Sign Up')


class UserSearch(FlaskForm):
    username_search = StringField('Search for a player',
                                  validators=[DataRequired()])
    submit = SubmitField('Search')
