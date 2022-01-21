from tinydb import TinyDB, Query
from tinydb.queries import where

from models.round_model import Round

db = TinyDB('database.json')
table = db.table('tournaments')
q = Query()


class Tournament():

    def __init__(self, name: str, location: str, game_format: str,
                 description: str, date_start, date_end=None,
                 rounds=None, players=None, total_rounds=4):
        self.name = name
        self.location = location
        self.game_format = game_format
        self.description = description
        self.date_start = date_start
        self.date_end = date_end if date_end else date_start
        self.rounds = rounds if rounds else []
        self.players = players if players else []
        self.total_rounds = total_rounds

    def __repr__(self) -> str:
        players_string = None
        if self.players:
            players_string = 'players: '
            for player in self.players:
                players_string += (
                    f"| {player['surname']} {player['first_name']} |")
        str_ = (
            f"name: {self.name}, location: {self.location}, "
            f"format: {self.game_format}, description: {self.description}, "
            f"starting date: {self.date_start}, ending date: {self.date_end}")
        if players_string:
            str_ += f"\n{players_string}"
        return str_

    def serialize(self) -> dict:
        tournament = {
            'name': self.name,
            'location': self.location,
            'description': self.description,
            'game_format': self.game_format,
            'date_start': self.date_start,
            'date_end': self.date_end,
            'rounds': self.rounds,
            'players': self.players,
            'total_rounds': self.total_rounds
            }
        return tournament

    def insert(self):
        tournament = self.serialize()
        table.insert(tournament)
        return tournament

    @classmethod
    def deserialize(cls, tournament):
        t = Tournament(tournament['name'], tournament['location'],
                       tournament['game_format'], tournament['description'],
                       tournament['date_start'], tournament['date_end'],
                       tournament['rounds'], tournament['players'])
        return t

    @classmethod
    def get_tournaments_in_db(cls) -> list:
        list_tournaments = []
        for tournament in table.all():
            list_tournaments.append(Tournament.deserialize(tournament))
        return list_tournaments

    @classmethod
    def delete_all_tournaments(cls):
        table.truncate()

    def delete_a_tournament(self):
        table.remove(where('name') == self.name)

    def add_round_to_tournament(self, round: Round):
        self.rounds.append(round)
        self.update()

    def update_round_results_in_tournament_db(self, game_result, game_index):

        self.get_last_round()['games'][game_index] = game_result

        players = self.players
        for player in players:
            if (player['surname'] == game_result[0][0]['surname'] or
                    player['surname'] == game_result[1][0]['surname']):
                player_index = player.index(players)
                self.players[player_index] = player

        self.update()

    def add_player_to_tournament(self, player: object):
        self.players.append(player.serialize())
        self.update()

    def end_round_in_tournament_db(self, end_date):
        self.rounds[-1]['end_date'] = end_date
        table.update(self.serialize(), q.name == self.name)

    def update(self):
        table.update(self.serialize(), q.name == self.name)

    def has_started(self) -> bool:
        if self.rounds:
            return True
        return False

    def has_ended(self):
        if len(self.rounds) == 4:
            if self.get_last_round().has_ended() is True:
                return True
        return False

    def is_full(self):
        if len(self.players) < 8:
            return False
        return True

    def get_last_round(self):
        return Round.deserialize(self.rounds[-1])

    def get_rounds(self):
        rounds = []
        for r in self.rounds:
            rounds.append(r)
        return rounds

    def player_count(self):
        return len(self.players)
