from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, NumberRange, InputRequired


class SubmitData(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    kills = IntegerField('Kills', validators=[
                         InputRequired("Please enter a whole number."),
                         NumberRange(min=0, max=75)])

    deaths = IntegerField('Deaths', validators=[
                          InputRequired("Please enter a whole number."),
                          NumberRange(min=0, max=10)])
    MMR = IntegerField('MMR/ELO after game', validators=[
                       InputRequired("Please enter a whole number."),
                       NumberRange(min=0, max=15000)])
    submit = SubmitField('Submit Data')


class Signup(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    image = FileField('Profile Image [.jpg, .png]', validators=[
                      FileRequired('Please upload a profile image'),
                      FileAllowed(['jpg', 'png'], '.jpg or .png only!')])
    submit = SubmitField('Sign Up')


class UserSearch(FlaskForm):
    username_search = StringField(validators=[DataRequired()],
                                  render_kw={
                                  "placeholder": "Search for a user"})
    submit = SubmitField('Search')


class DeleteProfile(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    delete_check = StringField('''Are you sure you want to delete your account
                               and any data attached to it?''',
                               validators=[DataRequired(
                                "Please enter your username.")], render_kw={
                                "placeholder": "Enter your username to confirm"
                                })
    submit = SubmitField('Delete Account')
