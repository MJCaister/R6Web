import sqlite3


# def leaderboard():
conn = sqlite3.connect('db/r6web.db')
cur = conn.cursor()
cur.execute('''SELECT * FROM SubmitedData;''')
allData = cur.fetchall()
print(allData[0, 3])
