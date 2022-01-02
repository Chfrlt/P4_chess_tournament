from tinydb import TinyDB, Query
from tinydb.operations import add

from models.round_model import Round



db = TinyDB('database.json')
table = db.table('tournaments')
q = Query()

class Tournament():

    def __init__(self, name : str, location : str, game_format : str,
    description : str, date_start, date_end = None, rounds = None, players = None):
        self.name = name
        self.location = location
        self.game_format = game_format
        self.description = description
        self.date_start = date_start
        self.date_end = date_end if date_end else date_start
        self.rounds = rounds if rounds else []
        self.total_rounds = 4
        self.players = players if players else []


    def __repr__(self) -> str:
        players_string = ''
        for player in self.players:
            players_string += '| {} {} |'.format(player['surname'], player['first_name'])
        str_ = (
            '''name: {}, location: {}, format: {},
        description: {}, starting date :{}, ending date: {}, \nplayers: {}'''
        .format(self.name, self.location, self.game_format,
        self.description, self.date_start, self.date_end,
        players_string)
        )
        return str_


    def deserialize(tournament):
        t = Tournament(tournament['name'], tournament['location'], tournament['game_format'],
        tournament['description'], tournament['date_start'], tournament['date_end'], tournament['rounds'], tournament['players'])
        return t


    def get_tournaments_in_db():
        list_tournaments = []
        for tournament in table.all():
            list_tournaments.append(Tournament.deserialize(tournament))
        return list_tournaments


    def add_round_to_tournament(self, round: dict):
        for tour in table:
            if tour['name'] == self.name:
                tour['rounds'].append(round)
                table.update(tour, q.name == self.name)


    def insert(self):
        tournament = self.serialize()
        table.insert(tournament)
        return tournament


    def serialize(self):
        tournament = {
            'name': self.name,
            'location': self.location,
            'description': self.description,
            'game_format': self.game_format,
            'date_start': self.date_start,
            'date_end': self.date_end,
            'rounds': self.rounds,
            'players': self.players
            }
        return tournament


    def add_player_in_tournament_db(self, player):
        for tour in table.all():
            if self.name == tour['name']:
                tour['players'].append(player)
                table.update(tour, q.name == tour['name'])


    def update_round_results_in_tournament_db(self, game_result, game_index):
        for tour in table.all():
            if tour['name'] == self.name:
                break

        updated_games = []
        for i, game in enumerate(tour['rounds'][-1]['games']):
            if i == game_index:
                updated_games.append(game_result)
            else:
                updated_games.append(game)

        updated_rounds = []
        for i, round in enumerate(tour['rounds']):
            if i == len(tour['rounds']) - 1:
                round = Round(round['name'], updated_games, round['start_date'], round['end_date'])
                updated_rounds.append(round.serialize())
            else:
                updated_rounds.append(round)

        updated_players = []
        for player in tour['players']:
            if player['surname'] == game_result[0][0]['surname']:
                updated_players.append(game_result[0][0])
            elif player['surname'] == game_result[1][0]['surname']:
                updated_players.append(game_result[1][0])
            else:
                updated_players.append(player)

        table.update(
            {'rounds': updated_rounds, 'players': updated_players}, q.name == tour['name'])


    def end_round_in_tournament_db(self, end_date):
        self.rounds[-1]['end_date'] = end_date
        table.update(self, q.name == self.name)


    def find_tournament(self):
        for t in table:
            if t['name'] == self.name:
                return t


    def delete_all_tournaments():
        table.truncate()