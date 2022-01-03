from tinydb import TinyDB, Query
from tinydb.queries import where


db = TinyDB('database.json')
table = db.table('players')
q = Query()


class Player():

    def __init__(self, first_name: str, surname: str,
                 birthdate: str, gender: str, elo: int,
                 score: float = None):
        self.first_name = first_name
        self.surname = surname
        self.birthdate = birthdate
        self.gender = gender
        self.elo = self.is_valid_elo(elo)
        self.score = score if score else 0.0

    def __repr__(self) -> str:
        '''Represent class object as a string'''
        player_string = (
            f"{self.surname} {self.first_name} | Elo: {self.elo} | "
            f"Gender: {self.gender}, birthdate: {self.birthdate}")
        if self.score != 0:
            player_string += f", score: {self.score}"
        return player_string

    @staticmethod
    def is_valid_elo(elo):
        if elo:
            try:
                int(elo)
                if int(elo) <= 0:
                    raise ValueError
                else:
                    return int(elo)
            except ValueError:
                raise ValueError

    @staticmethod
    def get_players_in_db() -> list:
        '''Return a list of all players in database'''
        list_players = []
        for player in table.all():
            list_players.append(Player.deserialize(player))
        return list_players

    @staticmethod
    def deserialize(player: dict) -> object:
        '''Transform a player class dict into a class object'''
        p = Player(player['first_name'], player['surname'],
                   player['birthdate'], player['gender'],
                   player['elo'], player['score'])
        return p

    @staticmethod
    def delete_all_players():
        table.truncate()

    def delete_a_player(self):
        table.remove(where('surname') == self.surname)

    def serialize(self) -> dict:
        '''Transform a class object into a dict'''
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
        'Serialize a player and insert it in database'
        player = self.serialize()
        table.insert(player)

    def update_player_in_db(self, updated_key):
        'Update values of a player object in database'
        if updated_key == 'surname':
            table.update(self.serialize(), q.birthdate == self.birthdate)
        else:
            table.update(self.serialize(), q.surname == self.surname)
