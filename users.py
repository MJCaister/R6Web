from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, NumberRange, ValidationError


class SubmitData(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    kills = FloatField('Kills', validators=[
                         DataRequired("Please enter a whole number."),
                         NumberRange(-1, 75)])

    deaths = FloatField('Deaths', validators=[
                          DataRequired("Please enter a whole number."),
                          NumberRange(-1, 10)])
    MMR = FloatField('MMR/ELO after game', validators=[
                       DataRequired("Please enter a whole number."),
                       NumberRange(-1, 15000)])
    submit = SubmitField('Submit Data')


def integer_check(form, field):
    data = int(field.data)
    if data < 0:
        raise ValidationError('Please enter a number that is 0 or higher')


class Signup(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    image = FileField('Profile Image [.jpg, .png]', validators=[
                      FileRequired('Please upload a profile image'),
                      FileAllowed(['jpg', 'png'], '.jpg or .png only!')])
    submit = SubmitField('Sign Up')


class UserSearch(FlaskForm):
    username_search = StringField('Search for a player',
                                  validators=[DataRequired()])
    submit = SubmitField('Search')
