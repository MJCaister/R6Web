from flask import Flask, render_template, flash, redirect, url_for
from users import SubmitData, Signup, UserSearch
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import sqlite3
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '/trailing_slashes/'


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html", page_title="Home")


@app.route('/leaderboard')
def leaderboard():
    return render_template("leaderboard.html", page_title="Leaderboard")


@app.route('/search', methods=['GET', 'POST'])
def search():
    conn = sqlite3.connect('db/r6web.db')
    cur = conn.cursor()
    form = UserSearch()
    if form.validate_on_submit():
        cur.execute('''SELECT username FROM ProfileInformation
                    WHERE username LIKE ('%{}%')'''.format(
                    form.username_search.data))
        search = cur.fetchone()
        if search is None:
            flash("No users found.")
            return redirect(url_for('search'))
        return redirect(url_for('search_results', search=search[0]))
    return render_template("search.html", page_title="Profile", form=form)


@app.route('/search_results/<search>', methods=['GET', 'POST'])
def search_results(search):
    conn = sqlite3.connect('db/r6web.db')
    cur = conn.cursor()
    form = UserSearch()
    if form.validate_on_submit():
        cur.execute('''SELECT username FROM ProfileInformation
                    WHERE username LIKE ('%{}%')'''.format(
                    form.username_search.data))
        search = cur.fetchone()
        if search is None:
            flash("No users found.")
            return redirect(url_for('search'))
    cur.execute('''SELECT profile_image FROM ProfileInformation
                WHERE username = '{}' '''.format(search))
    image = cur.fetchone()
    return render_template("results.html",
                           page_title="Search for {}".format(search),
                           search=search, image=image)


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = SubmitData()
    if form.validate_on_submit():
        conn = sqlite3.connect('db/r6web.db')
        cur = conn.cursor()
        cur.execute('''SELECT username FROM ProfileInformation
                    WHERE username = ('{}');'''.format(form.username.data))
        un = cur.fetchone()
        if un is None:
            flash("Invalid username or password.")
            return redirect(url_for('submit'))
        cur.execute('''SELECT password_hash FROM ProfileInformation
                    WHERE username = ('{}');'''.format(form.username.data))
        pw = cur.fetchone()
        cur.execute('''SELECT id FROM ProfileInformation
                    WHERE username = "{}"'''.format(form.username.data))
        unid = cur.fetchone()
        cur.execute('''INSERT INTO SubmitedData (pid, kills, deaths, MMR)
                    VALUES ('{}', '{}', '{}', '{}');'''.format(
                    unid[0], form.kills.data, form.deaths.data,
                    form.MMR.data))
        if un[0] is None or not check_password_hash(pw[0], form.password.data):
            flash('Invalid username or password.')
            return redirect(url_for('submit'))
        conn.commit()
        flash('Succesfully submited data.')
        return redirect(url_for('home'))
    return render_template('submitdata.html', page_title="Submit Data",
                           form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    conn = sqlite3.connect('db/r6web.db')
    cur = conn.cursor()
    form = Signup()
    if form.validate_on_submit():
        cur.execute('''SELECT username FROM ProfileInformation WHERE
                    username = '{}' '''.format(form.username.data))
        user = cur.fetchone()
        if user is not None:
            flash("A user with that name already exists, please use another")
            return redirect(url_for('signup'))
        flash('Signup requested for {}.'.format(form.username.data))
        f = form.image.data
        print(form.image.data)
        upload = str(form.image.data)
        fext = upload[-21:-17]
        fname = form.username.data + fext
        filename = secure_filename(fname)
        f.save(os.path.join(app.instance_path,
                            "H:/Programming/R6WEB/static/images/profiles/",
                            filename))
        cur.execute('''INSERT INTO ProfileInformation (username, password_hash,
                    profile_image) VALUES ('{}', '{}', '{}');'''.format(
                    form.username.data, generate_password_hash(
                        form.password.data),
                    "/static/images/profiles/" + filename))
        conn.commit()
        return redirect(url_for('signup'))
    return render_template('signup.html', page_title="Sign Up", form=form)


@app.route('/user/<user>')
def user(user):
    conn = sqlite3.connect('db/r6web.db')
    cur = conn.cursor()
    cur.execute('''SELECT profile_image FROM ProfileInformation
                WHERE username = '{}' '''.format(user))
    results = cur.fetchone()
    return render_template('user.html', page_title=user, user=user,
                           results=results)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.context_processor
def inject_search():
    searchform = UserSearch()
    return dict(searchform=searchform)


if __name__ == "__main__":
    app.run(debug=False, host="localhost", port=8080)
