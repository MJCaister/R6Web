from flask import Flask, render_template, flash, redirect, url_for
from users import Login, Signup
from flask_login import LoginManager, login_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3


app = Flask(__name__)
app.config['SECRET_KEY'] = '/trailing_slashes/'
login = LoginManager(app)


@app.route('/')
def home():
    return render_template("home.html", page_title="Home")


@app.route('/leaderboard')
def leaderboard():
    return render_template("leaderboard.html", page_title="Leaderboard")


@app.route('/profile/')
def profile():
    return render_template("profile.html", page_title="Profile")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Login()
    if form.validate_on_submit():
        conn = sqlite3.connect('db/r6web.db')
        cur = conn.cursor()
        cur.execute('''SELECT username FROM ProfileInformation
                    WHERE username =('{}');'''.format(form.username.data))
        un = cur.fetchone()
        cur.execute('''SELECT password_hash FROM ProfileInformation
                    WHERE username = ('{}');'''.format(form.username.data))
        pw = cur.fetchone()
        if un[0] is None or not check_password_hash(pw[0], form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        print("logged in")
        return redirect(url_for('home'))
    return render_template('login.html', page_title="Sign In", form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    conn = sqlite3.connect('db/r6web.db')
    cur = conn.cursor()
    form = Signup()
    if form.validate_on_submit():
        flash('Signup requested for {}'.format(
              form.username.data))
        cur.execute("INSERT INTO ProfileInformation (username, password_hash)"
                    "VALUES ('{}', '{}');".format(form.username.data,
                                                  generate_password_hash(
                                                    form.password.data)))
        conn.commit()
        return redirect(url_for('login'))
    return render_template('signup.html', page_title="Sign Up", form=form)


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=8080)
