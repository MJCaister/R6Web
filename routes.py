from flask import Flask, render_template
import sqlite3


app = Flask(__name__)


@app.route('/')
def home():
    return render_template("home.html", page_title="Home")


@app.route('/leaderboard')
def leaderboard():
    return render_template("leaderboard.html", page_title="Leaderboard")


@app.route('/profile/')
def profile():
    return render_template("profile.html", page_title="Profile")


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=8080)
