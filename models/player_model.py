from tinydb import TinyDB, Query


db = TinyDB('database.json')
table = db.table('players')
q = Query()


class Player():
    def __init__(self, first_name, surname, birthdate, gender, elo, score = None):
        self.first_name = first_name
        self.surname = surname
        self.birthdate = birthdate
        self.gender = gender
        self.elo = elo
        self.score = score if score else float(0)


    def __repr__(self):
        str_ = (
            """first name: {}, surname: {},
            birthdate: {}, gender: {}, elo: {})"""
            .format(self.first_name, self.surname,
            self.birthdate, self.gender, self.elo)
        )
        return str_


    def get_players_in_db():
        list_players = []
        for player in table.all():
            list_players.append(Player.deserialize(player))
        return list_players



    def deserialize(player):
        p = Player(player['first_name'], player['surname'], player['birthdate'],
            player['gender'], player['elo'], player['score'])
        return p


    def serialize(self):
        player = {
        'first_name': self.first_name,
        'surname': self.surname,
        'birthdate': self.birthdate,
        'gender': self.gender,
        'elo': self.elo,
        'score': self.score
        }
        return player


    def insert(self):
        player = self.serialize()
        table.insert(player)


    def update_elo(self, new_elo):
        table.update({'elo': new_elo}, q.surname == self.surname)


    def delete_all_players():
        table.truncate()