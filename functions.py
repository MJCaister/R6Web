import sqlite3


def Leaderboard():
    sorted = {}
    mmr_list = []

    def dictionary(id, mmr):
        sorted.update({id: mmr})
        mmr_list.append(mmr)
        print("sorted")
        print(sorted)

    conn = sqlite3.connect('db/r6web.db')
    cur = conn.cursor()
    # Credit: Bob for helping with queries
    cur.execute('''SELECT id FROM ProfileInformation;''')
    results = cur.fetchall()
    print(results)
    for player in results:
        cur.execute('''SELECT id FROM SubmitedData WHERE pid = {}'''.format(
                                                                    player[0]))
        results = cur.fetchall()
        if len(results) == 0:
            continue
        print(results)
        id_list = []
        for result in results:
            id_list.append(result[0])
        print(id_list)
        id_list.sort()
        print(id_list)
        latest_id = id_list[len(id_list) - 1]
        cur.execute('''SELECT MMR FROM SubmitedData WHERE id = {}'''.format(
                                                                    latest_id))
        mmr = cur.fetchone()
        print(player[0])
        print(mmr[0])
        print("mmr")

        dictionary(player[0], mmr[0])

    placeslst = list(sorted)
    place = {}

    for player in sorted:
        print('key: {}, index: {}'.format(player, placeslst.index(player)+1))
        place.update({player: placeslst.index(player)+1})
        print(place)

    tupList = list(place.items())
    finalDict = {}
    finalList = {}
    print(tupList)
    for player in tupList:
        print("Posistion: {} | Player : {} | Player ELO: {}".format(player[1],
                                                                    player[0],
                                                                    mmr_list[
                                                       tupList.index(player)]))
        finalDict.update({player[1]: player[0], mmr_list[
                    tupList.index(player)]: mmr_list[tupList.index(player)]})
    print(finalDict)
    finalList = list(finalDict.items())
    print(finalList)
    print(finalList[0])
    print(finalList[1])


Leaderboard()
