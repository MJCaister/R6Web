import sqlite3


def leaderboard_sort():
    conn = sqlite3.connect('db/r6web.db')
    cur = conn.cursor()
    cur.execute('''SELECT ProfileInformation.username,
                SubmitedData.MMR FROM ProfileInformation
                JOIN SubmitedData on ProfileInformation.id = SubmitedData.pid
                GROUP BY ProfileInformation.username
                ORDER BY SubmitedData.MMR DESC''')  # Gets the latest data of all users and sorts it by descending order
    results = cur.fetchall()
    return results  # Returns the result to the route which called it
