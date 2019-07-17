from flask_table import Table, Col

class OverallProfileStats(Table):
    id = Col('Id', show=False)
    kills = Col('Kills')
    deaths = Col('Deaths')
    kdratio = Col('K/D')
    elo = Col('ELO')
