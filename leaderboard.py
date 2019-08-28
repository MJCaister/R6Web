import sqlite3


def leaderboard_sort():
    conn = sqlite3.connect('db/r6web.db')
    cur = conn.cursor()
    cur.execute('''SELECT DISTINCT ProfileInformation.username,
                SubmitedData.MMR FROM ProfileInformation
                JOIN SubmitedData on ProfileInformation.id = SubmitedData.pid
                ORDER BY SubmitedData.MMR DESC''')
    results = cur.fetchall()
    print(results)
    
    for player in results:



leaderboard_sort()  # AUTO RUN
