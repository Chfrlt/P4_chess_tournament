from datetime import datetime
from itertools import cycle

from controllers.tournament_controller import TournamentControl
from models.round_model import Round
from models.tournament_model import Tournament
import views.round_views


class RoundControl(TournamentControl):

    def __init__(self) -> None:
        pass

    def display_round_infos(self, round: Round, print_games: bool = False):
        """Games informations for the round"""
        if isinstance(round, dict):
            round = Round.deserialize(round)
        rnd_repr = repr(round)
        views.round_views.print_round(rnd_repr)
        if print_games is True:
            games_reprs = round.game_repr()
            views.round_views.print_game(games_reprs)

    def selector_game(self, round: Round):
        """Select a game to update"""
        self.display_round_infos(round, print_games=True)
        game_index = views.round_views.game_selector_view()
        return game_index

    def add_round_to_tournament(self, tournament: Tournament, round: Round):
        if isinstance(round, object):
            round = round.serialize()
        tournament.rounds.append(round)
        tournament.update()

    def create_round(self, tournament: Tournament):
        players_in_tournament_elo_sorted = (
            self.get_sorted_players_in_tournament(
                tournament, elo_sorted=True))
        players = self.players_sorter_for_round(
            players_in_tournament_elo_sorted)

        if tournament.has_started() is True:
            old_games = []
            for round in tournament.get_rounds():
                round = Round.deserialize(round)
                for game in round.games:
                    old_games.append([game[0], game[1]])
            new_games = self.past_first_round_pairings(players, old_games)

        else:
            new_games = self.first_round_pairings(players)
        new_round = Round(
            name='Round {}'.format(len(tournament.rounds) + 1),
            games=new_games,
            start_date=datetime.today().strftime('%Y-%m-%d %H:%M')
            )
        self.add_round_to_tournament(tournament, new_round)

    def players_sorter_for_round(self, players: list) -> list:
        '''From a list of players, sort the list for round pairings
        Players are sorted by score (higher to lower).
        If scores are equals, by elo (higher to lower)'''
        temp_players = players
        players_sorted = []

        while temp_players:
            head = temp_players[0]
            for p in temp_players:
                for i in temp_players:
                    if head['score'] < i['score']:
                        head = i
                    elif (head['elo'] < i['elo'] and
                          head['score'] == i['score']):
                        head = i
            players_sorted.append(head)
            temp_players.remove(head)
        return players_sorted

    def first_round_pairings(self, players) -> list:
        upper_half = players[:int(len(players) / 2)]
        lower_half = players[int(len(players) / 2):]
        new_games = []
        for i in range(int(len(players) / 2)):
            player1 = upper_half[i]
            player2 = lower_half[i]
            new_game = ([player1, 0.0], [player2, 0.0])
            new_games.append(new_game)
        return new_games

    def past_first_round_pairings(self, players: list,
                                  old_games: list) -> list:
        upper_half = players[:int(len(players) / 2)]
        lower_half = players[int(len(players) / 2):]
        upper_half.reverse()
        lower_half.reverse()

        for p in upper_half:
            p['opponents'] = []
        for i, p in enumerate(upper_half):
            for game in old_games:
                p1 = game[0][0]
                p2 = game[1][0]
                _is_index_0 = all([value == p[key]
                                  for key, value in p1.items()
                                  if key != 'score'])
                _is_index_1 = all([value == p[key]
                                  for key, value in p2.items()
                                  if key != 'score'])
                if _is_index_0 is True:
                    upper_half[i]['opponents'].append(game[1][0])
                elif _is_index_1 is True:
                    upper_half[i]['opponents'].append(game[0][0])

        new_games = []
        while lower_half:
            player1 = upper_half[0]
            player_iterator = cycle(lower_half)
            player2 = player_iterator.__next__()
            while player2 in player1['opponents']:
                if all(p in player1['opponents'] for p in lower_half) is True:
                    upper_half.append(new_games[-1][0][0])
                    lower_half.append(new_games[-1][1][0])
                    new_games.pop()
                else:
                    player2 = player_iterator.__next__()
                    break
            del player1['opponents']
            upper_half.remove(player1)
            lower_half.remove(player2)
            new_game = ([player1, 0], [player2, 0])
            new_games.append(new_game)
        return new_games

    def reset_game_results(self,
                           game: tuple) -> tuple:
        """Reset a game result to 0"""
        if game[0][1] == 1:
            game[0][0]['score'] -= 1
        elif game[0][1] == 0.5:
            game[0][0] -= 0.5
        if game[1][1] == 1:
            game[1][0]['score'] -= 1
        elif game[1][1] == 0.5:
            game[1][0]['score'] -= 0.5
        game[0][1] = 0
        game[1][1] = 0
        return game

    def update_game(self, game_index: int, tournament: Tournament):
        '''From index reference, update a tournament game result and
        the associated players scores using user input.
        Update in db.'''
        games_in_round = tournament.get_last_round().games
        game = games_in_round[game_index]
        player1 = game[0][0]
        player2 = game[1][0]
        for i, p in enumerate(tournament.players):
            if p['surname'] == player1['surname']:
                p1_index = i
            elif p['surname'] == player2['surname']:
                p2_index = i
        result = views.round_views.update_game_view(game_index,
                                                    player1, player2)
        if result == -1:
            return
        elif result == 0:
            game[0][0]['score'] += 1
            game[0][1] = 1
            game[1][1] = 0
        elif result == 1:
            game[1][0]['score'] += 1
            game[0][1] = 0
            game[1][1] = 1
        elif result == 2:
            game[0][0]['score'] += 0.5
            game[1][0]['score'] += 0.5
            game[0][1] = 0.5
            game[1][1] = 0.5
        elif result == 3:
            game = self.reset_game_results(game)
        tournament.players[p1_index] = game[0][0]
        tournament.players[p2_index] = game[1][0]
        tournament.get_last_round().games[game_index] = game
        tournament.update()

    def end_round(self, tournament: Tournament):
        """End a round, update in db"""
        if tournament.get_last_round().has_ended() is False:
            end_date = datetime.today().strftime('%Y-%m-%d %H:%M')
            tournament.end_round_in_tournament_db(end_date)
