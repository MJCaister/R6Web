from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import (DataRequired, NumberRange, InputRequired,
                                EqualTo)


class SubmitData(FlaskForm):
    # Makes sure the user inputs data and sets a disapearing text inside of the input field html
    username = StringField('Username', validators=[DataRequired()],
                           render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[DataRequired()],
                             render_kw={"placeholder": "Password"})
    # Makes sure that the user submits a valid value
    kills = IntegerField('Kills', validators=[
                         InputRequired("Please enter a whole number."),
                         NumberRange(min=0, max=75)],
                         render_kw={"placeholder": "Kills"})
    deaths = IntegerField('Deaths', validators=[
                          InputRequired("Please enter a whole number."),
                          NumberRange(min=0, max=10)],
                          render_kw={"placeholder": "Deaths"})
    MMR = IntegerField('MMR/ELO after game', validators=[
                       InputRequired("Please enter a whole number."),
                       NumberRange(min=0, max=15000)],
                       render_kw={"placeholder": "MMR/ELO"})
    submit = SubmitField('Submit Data')


class Signup(FlaskForm):
    username = StringField('Username', validators=[DataRequired()],
                           render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[DataRequired()],
                             render_kw={"placeholder": "Password"})
    password_confirm = PasswordField('Confirm Password', validators=[
                                    DataRequired(), EqualTo(
                                        'password',
                                        message='Passwords must match.')],
                                     render_kw={"placeholder":
                                     "Confirm Password"})
    # Checks that the users uploaded image is only of the file types .jpg or .png and makes sure that the user submits a image
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
    username = StringField('Username', validators=[DataRequired()],
                           render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[DataRequired()],
                             render_kw={"placeholder": "Password"})
    delete_check = StringField('''Are you sure you want to delete your account
                               and any data attached to it?''',
                               validators=[DataRequired(
                                "Please enter your username.")], render_kw={
                                "placeholder": "Enter your username to confirm"
                                })
    submit = SubmitField('Delete Account')
