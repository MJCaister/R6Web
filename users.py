from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_login import UserMixin
import sqlite3


class Login(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class Signup(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')


class User(UserMixin):
    def __init__(self, username, password):
        self.username = username.lower()
        self.password = password

    def is_authenticated():
        return True

    def is_active():
        return True

    def get_id(self):
        conn = sqlite3.connect('db/r6web')
        cur = conn.cursor()
        cur.execute('''SELECT id FROM ProfileInformation
                    WHERE username = "{}"'''.format(self.username))
        return int(cur.fetchone())
