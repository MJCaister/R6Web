from flask import Flask, render_template, flash, redirect, url_for
from users import SubmitData, Signup, UserSearch, DeleteProfile
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import sqlite3
import os
from leaderboard import leaderboard_sort
# Importing dependency librarys and leaderboard function


# File System Management is used to set the file location of
# Start of Different File System Management
school_dir = False
instancepath = None
development_build = True

if development_build is True:
    if school_dir is True:
        instancepath = "H:/Programming/R6WEB/"
    else:
        instancepath = "C:/Users/nukes/Desktop/Git Desktop/R6Web/"
else:
    instancepath = "/home/Predictive/R6Web"
# End of File System Management

# Flask Config
app = Flask(__name__, instance_path=instancepath)  # sets the variable app with the Flask function to set the instance path
app.config['SECRET_KEY'] = '/trailing_slashes/'  # Sets the secret key of the flaskapp

# Checks if the flaskapp is running inside of development mode to then show the directory
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
@app.route('/', methods=['GET', 'POST'])  # Creates a route for the flaskapp for the home route
def home():
    return render_template("home.html", page_title="Home")  # reture the render template function to the user so that they can see the html file, and add the title Home to the tab


@app.route('/leaderboard')
def leaderboard():
    list = leaderboard_sort()  # assigns the returned value from the imported function leaderboard_sort
    return render_template("leaderboard.html", page_title="Leaderboard",
                           list=list)  # adds the variable to the page for jinja2 templating


@app.route('/search_results', methods=['POST'])  # POST method for form submissions
def search_results():
    conn = sqlite3.connect('db/r6web.db')  # connects to the database file
    cur = conn.cursor()  # assigns the connections cursor
    form = UserSearch()  # assigns the data from the forms class
    search = {}  # empty tuple
    search_raw = form.username_search.data  # assigns the users search to the variable
    if form.validate_on_submit():  # Checks if the form was submitted
        if form.username_search.data is None:  # Checks if the user searched for nothing
            flash("No users found.")  # Sends a flash message to the user
        try:
            cur.execute('''SELECT username, profile_image FROM
                        ProfileInformation WHERE username LIKE
                        ('%{}%')'''.format(form.username_search.data))  # Executes a SQL query for the users search, looks for similiar searches
            search = cur.fetchall()  # Assigns the results to a tuple
        except TypeError:  # Checks for user entering Type None in search
            flash("No users found.")
        if not len(search) > 0:  # Checks if the len of the search is not greater than 0
            flash("No users found.")
        return render_template("results.html",
                               page_title="User Search for {}".format(
                                   form.username_search.data), search=search,
                               search_raw=search_raw)  # Returns render template with search tuple and raw search input
    flash("No Results Found.")
    return render_template("results.html", page_title="No Results Found")  # Returns for when no results found


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = SubmitData()
    if form.validate_on_submit():
        conn = sqlite3.connect('db/r6web.db')
        cur = conn.cursor()
        cur.execute('''SELECT username FROM ProfileInformation
                    WHERE username = ('{}');'''.format(form.username.data))
        un = cur.fetchone()
        if un is None:  # Checks if the username exists in the database
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
        if deaths == 0:  # Checks for deaths equals zero to avoid div by zero
            kdr = kills
            con_kdr = kdr
        else:
            kdr = kills / deaths  # Calculates a float value
            con_kdr = round(kdr, 2)  # Rounds the float value to 2 decimals
        cur.execute('''INSERT INTO SubmitedData (pid, kills, deaths, kdr, MMR)
                    VALUES ('{}', '{}', '{}', '{}', '{}');'''.format(
                    unid[0], form.kills.data, form.deaths.data, con_kdr,
                    form.MMR.data))  # Executes a query inserting a new row into the table for all the calculated data
        if un[0] is None or not check_password_hash(pw[0], form.password.data):  # Checks if username exists or if the password hash is not returned as true
            flash('Invalid username or password.')
            return redirect(url_for('submit'))  # Returns the user back to the same web URL
        conn.commit()  # Commits inserted values into database
        flash('Succesfully submited data.')
        return redirect(url_for('home'))  # Redirects user back to the home page
    return render_template('submitdata.html', page_title="Submit Data",
                           form=form)  # Sends the form for jinja templating


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
        f = form.image.data  # Assigns the uploaded file information to a variable
        upload = str(form.image.data)  # Converts the uploaded image data into a string
        fext = upload[-21:-17]  # F(ile)ext(ension) is set equal to the file extension of the uploaded image
        fname = form.username.data + fext  # The file name is assigned as the username plus the image file extension
        filename = secure_filename(fname)  # Makes the filename secure
        f.save(os.path.join(app.instance_path, "static/images/profiles/",
                            filename))  # Saves the image to the webapps path for images
        cur.execute('''INSERT INTO ProfileInformation (username, password_hash,
                    profile_image) VALUES ('{}', '{}', '{}');'''.format(
                    form.username.data, generate_password_hash(
                        form.password.data),  # Creates a Salted SHA256 hash of the users password for security
                    "/static/images/profiles/" + filename))  # Inserts the new users information into the database table for users
        conn.commit()
        return redirect(url_for('signup'))
    return render_template('signup.html', page_title="Sign Up", form=form)


@app.route('/user/<user>')
def user(user):  # Parses conext from the url
    conn = sqlite3.connect('db/r6web.db')
    cur = conn.cursor()
    cur.execute('''SELECT profile_image FROM ProfileInformation
                WHERE username = '{}';'''.format(user))
    results = cur.fetchone()
    cur.execute('''SELECT username, kills, deaths, kdr, MMR
                FROM SubmitedData AS S INNER JOIN ProfileInformation
                AS P ON S.pid = P.id WHERE P.username = '{}';'''.format(user))  # Retreives users match history from database
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
        if credentials is None or not check_password_hash(credentials[1],
                                                          form.password.data
                                                          ):
            flash('''Invalid username/password or this account
                  has already been deleted.''')
            return redirect(url_for('delete'))
        if form.delete_check.data != form.username.data:  # Checks the username against the delete checker to prevent accidental deletions of accounts
            flash('Incorrect username was provided for the check.')
            return redirect(url_for('delete'))
        cur.execute('''SELECT profile_image FROM ProfileInformation WHERE
                    username = '{}';'''.format(form.username.data))
        imageLoc = cur.fetchone()
        try:
            os.remove(app.instance_path + imageLoc[0])  # Try to delete users image file
        except OSError as e:
            print(e)  # If file does not exist, return the error to console
        cur.execute('''SELECT id FROM ProfileInformation WHERE
                    username = ('{}');'''.format(form.username.data))
        uid = cur.fetchone()
        cur.execute('''DELETE FROM ProfileInformation
                    WHERE username = '{}';'''.format(form.username.data))
        cur.execute('''DELETE FROM SubmitedData WHERE
                    pid = {};'''.format(uid[0]))  # Deletes data against the users ID
        conn.commit()
        flash('Sucessfully deleted data for user: {}'.format(
              form.username.data))
        return redirect(url_for('home'))
    return render_template('delete.html', page_title="Delete Account",
                           form=form)


@app.errorhandler(404)  # Checks for 404 error in the error handler
def page_not_found(e):
    return render_template('404.html'), 404  # Returns the 404 page


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.context_processor  # Allows the search form to be accessible
def inject_search():
    searchform = UserSearch()
    return dict(searchform=searchform)  # Returns the form as a dictionary


if __name__ == "__main__":  # Checks if the webapp name is correct
    app.run(debug=True, host="localhost", port=8080)  # Initiates the application with the host name and the port
