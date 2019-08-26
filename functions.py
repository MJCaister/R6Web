import sqlite3


def leaderboard_sort():
    sorted = {}
    mmr_list = []

    def dictionary(id, mmr):
        sorted.update({id: mmr})
        mmr_list.append(mmr)

    conn = sqlite3.connect('db/r6web.db')
    cur = conn.cursor()
    # Credit: Bob for helping with queries
    cur.execute('''SELECT id FROM ProfileInformation;''')
    results = cur.fetchall()
    for player in results:
        cur.execute('''SELECT id FROM SubmitedData WHERE pid = {}'''.format(
                                                                    player[0]))
        results = cur.fetchall()
        if len(results) == 0:
            continue
        id_list = []
        for result in results:
            id_list.append(result[0])
        id_list.sort()
        latest_id = id_list[len(id_list) - 1]
        cur.execute('''SELECT MMR FROM SubmitedData WHERE id = {}'''.format(
                                                                    latest_id))
        mmr = cur.fetchone()

        dictionary(player[0], mmr[0])

    placeslst = list(sorted)
    place = {}

    for player in sorted:
        place.update({player: len(sorted)-placeslst.index(player)})

    tupList = list(place.items())
    print(tupList)
    finalList = []
    for player in tupList:
        cur.execute('''SELECT username FROM ProfileInformation
                    WHERE id={}'''.format(player[0]))
        name = cur.fetchone()
        user = {'Rank': player[1], 'Name': name[0],
                'MMR': mmr_list[tupList.index(player)]}
        finalList.append(user)
    print(finalList)
    return finalList


# leaderboard()  # AUTO RUN
