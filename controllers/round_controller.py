from datetime import datetime

from models.tournament_model import Tournament
from views.round_views import RoundView
from models.round_model import Round

class RoundControl:

    def show_games(tournament):
        """Games informations for the round"""
        if tournament.rounds:
            games = tournament.rounds[-1]['games']
            for i, game in enumerate(games):
                player1 = game[0][0]
                player2 = game[1][0]
                score1 = game[0][1]
                score2 = game[1][1]
                RoundView.print_game(i, player1, player2, score1, score2)


    def selector_game(tournament):
        """Get input game to update"""
        max_index = len(tournament.rounds[-1]['games'])
        RoundControl.show_games(tournament)
        while True:
            selection = RoundView.game_selector_view()
            try:
                game_selection = int(selection) - 1
                if game_selection < 0 or game_selection > max_index:
                    continue
                break
            except ValueError:
                continue
        return game_selection



    def create_first_round(tournament):
        players_elo_sorted = sorted(tournament.players, key=lambda x: x['elo'])

        upper = players_elo_sorted[:int(len(players_elo_sorted) / 2)]
        lower = players_elo_sorted[int(len(players_elo_sorted) / 2):]
        games = []
        for i in range(int(len(players_elo_sorted) / 2)):
            player1 = upper[i]
            player2 = lower[i]
            game = ([player1, 0], [player2, 0])
            print(games)
            games.append(game)
        round = Round(
            name = 'Round {}'.format(len(tournament.rounds) + 1),
            games = games,
            start_date = datetime.today().strftime('%Y-%m-%d %H:%M')
        )
        tournament.add_round_to_tournament(round.serialize())


    def reset_game_results(game):
        """Reset game score to null"""
        if game[0][1] == 1:
            game[0][0][0]['score'] -= 1
        elif game[0][1] == 0.5:
            game[0][0][0]['score'] -= 0.5
        if game[1][1] == 1:
            game[1][0][0]['score'] -= 1
        elif game[1][1] == 0.5:
            game[1][0][0]['score'] -= 0.5
        game[0][1] = 0
        game[1][1] = 0
        return game


    def update_game(game_index: int, tournament: Tournament):
        '''Update a game result and players scores. Update to db
        [1] player1 win
        [2] player2 win
        [3] Draw game
        [4] Reset results
        [0] Cancel'''
        game = tournament.rounds[-1]['games'][game_index]
        player1 = game[0][0]
        player2 = game[1][0]
        while True:
            result_input = RoundView.update_game_view(game_index, player1, player2)
            try:
                game_result = int(result_input)
                if game_result > 0 and game_result < 5:
                    if game_result == 1:
                        game[0][0]['score'] += 1
                        game[0][1] = 1
                        game[1][1] = 0
                    elif game_result == 2:
                        game[1][0]['score'] += 1
                        game[0][1] = 0
                        game[1][1] = 1
                    elif game_result == 3:
                        game[0][0]['score'] += 0.5
                        game[1][0]['score'] += 0.5
                        game[0][1] = 0.5
                        game[1][1] = 0.5
                    elif game_result == 4:
                        game = RoundControl.reset_game_results(game)
                    tournament.update_round_results_in_tournament_db(game, game_index)
                    break
                elif game_result == 0:
                    break
            except ValueError:
                continue


    def end_round(tournament: Tournament):
        """End round, update in db"""
        tournament.rounds[-1]['end_date'] = datetime.today().strftime('%Y-%m-%d %H:%M')
        for game in tournament.rounds['games']:
            game_tuple = tuple(zip([game['player1'], game['player2']], [game['score1'], game['score2']]))
            tournament.rounds[-1]['games'].append(game_tuple)
        tournament.end_round_in_tournament_db(tournament)