import sqlite3


# def leaderboard():
conn = sqlite3.connect('db/r6web.db')
cur = conn.cursor()
# Credit: Bob for helping with queries
cur.execute('''SELECT id FROM ProfileInformation;''')
results = cur.fetchall()
for player in results:
    cur.execute('''''')
 
