from tinydb import TinyDB, Query

db = TinyDB('database.json')
q = Query()

class Round():
    def __init__(self, name, games, start_date, end_date = None):
        self.name = name
        self.games = games
        self.start_date = start_date
        self.end_date = end_date if end_date else ""


    def serialize(self):
        round = {'name': self.name,
        'games': self.games,
        'start_date': self.start_date,
        'end_date': self.end_date}
        return round


    def deserialize(round):
        r = Round(round['name'], round['games'], round['start_date'], round['end_date'])


    def __repr__(self):
        str_ = (
            '''Round('{}', '{}', '{}', '{}')'''
            .format(self.name, self.start_date, self.end_date, self.games)
            )
        return str_