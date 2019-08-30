import sqlite3


def leaderboard_sort():
    conn = sqlite3.connect('db/r6web.db')
    cur = conn.cursor()
    cur.execute('''SELECT ProfileInformation.username,
                SubmitedData.MMR FROM ProfileInformation
                JOIN SubmitedData on ProfileInformation.id = SubmitedData.pid
                GROUP BY ProfileInformation.username
                ORDER BY SubmitedData.MMR DESC''')
    results = cur.fetchall()
    return results
