import sqlite3


def leaderboard_sort():
    sorted = {}

    def dictionary(id, mmr):
        sorted.update({id: mmr})
        print("Sorted: {}".format(sorted))

    conn = sqlite3.connect('db/r6web.db')
    cur = conn.cursor()
    # Credit: Bob for helping with queries
    cur.execute('''SELECT id FROM ProfileInformation;''')
    results = cur.fetchall()
    print("ID's: {}".format(results))
    for player in results:
        cur.execute('''SELECT id FROM SubmitedData WHERE pid = {}'''.format(
                                                                    player[0]))
        results = cur.fetchall()
        print("ID: {} | IDs: {}".format(player[0], results))
        if len(results) == 0:
            continue
        id_list = []
        for result in results:
            id_list.append(result[0])
            print("IDList: {}".format(id_list))
        id_list.sort()
        print("IDListSorted: {}".format(id_list))
        latest_id = id_list[len(id_list) - 1]
        print("LatestId: {}".format(latest_id))
        cur.execute('''SELECT MMR FROM SubmitedData WHERE id = {}'''.format(
                                                                    latest_id))
        mmr = cur.fetchone()
        print("Player: {} | MMR: {}".format(player[0], mmr))
        dictionary(player[0], mmr[0])
    placeslst = list(sorted)
    print("PLACELIST: {}".format(placeslst))
    place = {}

    for player in sorted:
        place.update({player: placeslst.index(player)+1})
    print("Place: {}".format(place))
    tupList = list(place.items())
    print("TupList: {}".format(tupList))
    finalList = []
    for player in tupList:
        cur.execute('''SELECT username FROM ProfileInformation
                    WHERE id={}'''.format(player[0]))
        name = cur.fetchone()
        user = {'Rank': player[1], 'Name': name[0],
                'MMR': sorted[player[0]]}
        finalList.append(user)
        print("User: {}".format(user))
    print("FinalList: {}".format(finalList))
    return finalList


leaderboard_sort()  # AUTO RUN
