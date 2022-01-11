from tinydb import TinyDB, Query

db = TinyDB('database.json')
q = Query()


class Round():

    def __init__(self, name: str, games: list,
                 start_date: str, end_date: str = None):
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

    @classmethod
    def deserialize(cls, round: dict) -> dict:
        r = Round(round['name'], round['games'],
                  round['start_date'], round['end_date'])
        return r

    def __repr__(self) -> str:
        if self.end_date:
            end_date_string = self.end_date
        else:
            end_date_string = 'In progress'
        rnd_str = (f"{self.name}, started: {self.start_date}, "
                   f"ended: {end_date_string}")
        return rnd_str

    def game_repr(self) -> str:
        games_as_strings = []
        for i, game in enumerate(self.games):
            player1 = game[0][0]
            player2 = game[1][0]
            score1 = game[0][1]
            score2 = game[1][1]
            game_str = f"== Game {i + 1} ==\n"
            game_str += (
                f"Player 1: {player1['surname']} {player1['first_name']}, "
                f"elo: {player1['elo']}\nvs\n"
                f"Player 2: {player2['surname']} {player2['first_name']}, "
                f"elo: {player2['elo']}")
            if score1 > score2:
                game_str += (f"\nResult: {player1['surname']} "
                             f"{player1['first_name']} WIN")
            elif score2 > score1:
                game_str += (f"\nResult: {player2['surname']} "
                             f"{player2['first_name']} WIN")
            elif score1 == 0.5:
                game_str += "\nResult: DRAW"
            games_as_strings.append(game_str)
        return games_as_strings

    def has_ended(self) -> bool:
        if self.end_date:
            if self.is_completed() is True:
                return True
        else:
            return False

    def is_completed(self):
        for game in self.games:
            if game[0][1] == 0 and game[1][1] == 0:
                return False
        return True

    def get_indexes_non_completed_games(self):
        if self.is_completed() is False:
            indexes = []
            for index, game in enumerate(self.games):
                if game[0][1] == 0 and game[1][1] == 0:
                    indexes.append(index)
            return indexes
