from flask import Flask, render_template, flash, redirect, url_for
from users import SubmitData, Signup, UserSearch, DeleteProfile
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import sqlite3
import os

# Start of Different File System Management
school_dir = True
instancepath = None
development_build = True

if development_build is True:
    if school_dir is True:
        instancepath = "H:/Programming/R6WEB/"
    else:
        instancepath = "C:/Users/nukes/Desktop/Git Desktop/R6Web/"
else:
    print()
# End of File System Management

# Flask Config
app = Flask(__name__, instance_path=instancepath)
app.config['SECRET_KEY'] = '/trailing_slashes/'

if development_build is True:
    print("\n")
    print("INSTANCE PATH: {}".format(app.instance_path))
    print("\n")
else:
    print("\n")
    print("RUNNING ON LIVE DIRECTORY")
    print("\n")
# End of Flask Config


# Start of Flask Routes
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html", page_title="Home")


@app.route('/leaderboard')
def leaderboard():

    return render_template("leaderboard.html", page_title="Leaderboard")


@app.route('/search_results', methods=['POST'])
def search_results():
    conn = sqlite3.connect('db/r6web.db')
    cur = conn.cursor()
    form = UserSearch()
    search = None
    if form.username_search.data is None:
        flash("No users found.")
    if form.validate_on_submit():
        cur.execute('''SELECT username, profile_image FROM ProfileInformation
                    WHERE username LIKE ('%{}%')'''.format(
                    form.username_search.data))
        search = cur.fetchall()
        if not len(search) > 0:
            flash("No users found.")
            return redirect(url_for('home'))
    return render_template("results.html",
                           page_title="User Search for {}".format(
                            form.username_search.data), search=search)


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
        kills = form.kills.data
        deaths = form.deaths.data
        con_kdr = None
        if deaths == 0:
            kdr = kills
            con_kdr = kdr
        else:
            kdr = kills / deaths
            con_kdr = round(kdr, 2)
        cur.execute('''INSERT INTO SubmitedData (pid, kills, deaths, kdr, MMR)
                    VALUES ('{}', '{}', '{}', '{}', '{}');'''.format(
                    unid[0], form.kills.data, form.deaths.data, con_kdr,
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
        f.save(os.path.join(app.instance_path, "static/images/profiles/",
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
                WHERE username = '{}';'''.format(user))
    results = cur.fetchone()
    cur.execute('''SELECT username, kills, deaths, kdr, MMR
                FROM SubmitedData AS S INNER JOIN ProfileInformation
                AS P ON S.pid = P.id WHERE P.username = '{}';'''.format(user))
    data = cur.fetchall()
    table = data
    return render_template('user.html', page_title=user, user=user,
                           results=results, table=table)


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    form = DeleteProfile()
    conn = sqlite3.connect('db/r6web.db')
    cur = conn.cursor()
    if form.validate_on_submit():
        cur.execute('''SELECT username, password_hash FROM ProfileInformation
                    WHERE username = ('{}');'''.format(form.username.data))
        credentials = cur.fetchone()
        if credentials[0] is None or not check_password_hash(credentials[1],
                                                             form.password.data
                                                             ):
            flash('Invalid username/password or this account has been deleted.'
                  )
            return redirect(url_for('delete'))
        if form.delete_check.data != form.username.data:
            flash('Incorrect username was provided for the check.')
            return redirect(url_for('delete'))
        cur.execute('''SELECT profile_image FROM ProfileInformation WHERE
                    username = '{}';'''.format(form.username.data))
        imageLoc = cur.fetchone()
        try:
            os.remove(app.instance_path + imageLoc[0])
        except OSError as e:
            print(e)
        cur.execute('''SELECT id FROM ProfileInformation WHERE
                    username = ('{}');'''.format(form.username.data))
        uid = cur.fetchone()
        cur.execute('''DELETE FROM ProfileInformation
                    WHERE username = '{}';'''.format(form.username.data))
        cur.execute('''DELETE FROM SubmitedData WHERE
                    pid = {};'''.format(uid[0]))
        conn.commit()
        flash('Sucessfully deleted data for user: {}'.format(
              form.username.data))
        return redirect(url_for('home'))
    return render_template('delete.html', page_title="Delete Account",
                           form=form)


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
