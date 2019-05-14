from flask import Flask, render_template, flash, redirect, url_for
from login import Login, passwords, Signup
from flask_login import LoginManager
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
    form = Login()
    if form.validate_on_submit():
        flash('Login Requested for user {}, remember_me={}'.format(
              form.username.data, form.remember_me.data))
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
        set_password(form.password.data)
        cur.execute("INSERT INTO ProfileInformation (username, password_hash) VALUES ('{}', '{}');".format(form.username.data, set_password.password_hash))
        conn.commit()
        return redirect(url_for('login'))
    return render_template('signup.html', page_title="Sign Up", form=form)


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=8080)
