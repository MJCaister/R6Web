from flask import Flask, render_template, flash, redirect, url_for
from users import SubmitData, Signup, UserSearch
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3


app = Flask(__name__)
app.config['SECRET_KEY'] = '/trailing_slashes/'


@app.route('/')
def home():
    return render_template("home.html", page_title="Home")


@app.route('/leaderboard')
def leaderboard():
    return render_template("leaderboard.html", page_title="Leaderboard")


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = UserSearch()
    if form.validate_on_submit():
        conn = sqlite3.connect('db/r6web')
        cur = conn.cursor()
        cur.execute('''SELECT username FROM ProfileInformation WHERE username = ('{}')'''.format(form.username_search.data))
        search = cur.fetchall()
        return redirect(url_for('search'), search=search)
    return render_template("search.html", page_title="Profile", form=form)


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = SubmitData()
    if form.validate_on_submit():
        conn = sqlite3.connect('db/r6web.db')
        cur = conn.cursor()
        cur.execute('''SELECT username FROM ProfileInformation
                    WHERE username = ('{}');'''.format(form.username.data))
        un = cur.fetchone()
        cur.execute('''SELECT password_hash FROM ProfileInformation
                    WHERE username = ('{}');'''.format(form.username.data))
        pw = cur.fetchone()
        cur.execute('''INSERT INTO SubmitedData (username, kills, deaths, MMR)
                    VALUES ('{}', '{}', '{}', '{}');'''.format(
                    form.username.data, form.kills.data, form.deaths.data,
                    form.MMR.data))
        if un[0] is None or not check_password_hash(pw[0], form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('submit'))
        conn.commit()
        return redirect(url_for('home'))
    return render_template('submitdata.html', page_title="Submit Data",
                           form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    conn = sqlite3.connect('db/r6web.db')
    cur = conn.cursor()
    form = Signup()
    if form.validate_on_submit():
        flash('Signup requested for {}'.format(
              form.username.data))
        cur.execute('''INSERT INTO ProfileInformation (username, password_hash)
                    VALUES ('{}', '{}');'''.format(form.username.data,
                                                   generate_password_hash(
                                                    form.password.data)))
        conn.commit()
        return redirect(url_for('signup'))
    return render_template('signup.html', page_title="Sign Up", form=form)


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=8080)
