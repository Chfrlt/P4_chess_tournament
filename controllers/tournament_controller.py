from datetime import datetime

from models.player_model import Player
from models.tournament_model import Tournament
from models.round_model import Round
from views.tournament_views import TournamentView


class TournamentControl:


    def selector():
        tournaments_list = Tournament.get_tournaments_in_db()
        TournamentView.selector_view(tournaments_list)
        selection_input = input()
        try:
            selection = int(selection_input)
            try:
                t = tournaments_list[selection - 1]
                return t
            except IndexError:
                TournamentView.print_message(
                    'Invalid input. Did not correspond to any item in the list')
        except ValueError:
            TournamentView.print_message('Invalid input: Was not a number.')
        

    def create_tournament():
        tournament_dict = TournamentView.creator_view()
        try:
            date_end_int = int(tournament_dict['date_end'])
            if date_end_int == 0:
                tournament_dict['date_end'] = tournament_dict['date_start']
        except ValueError:
            pass
        new_tournament = Tournament(
            tournament_dict['name'],
            tournament_dict['location'],
            tournament_dict['game_format'],
            tournament_dict['description'],
            tournament_dict['date_start'],
            tournament_dict['date_end']
        )
        return Tournament.insert(new_tournament)


    def add_player_to_tournament(player : Player, tournament: Tournament):
        tournament.add_player_in_tournament_db(player.serialize())


    def check_if_tournament_is_full(tournament):
        if len(tournament.players) < 7:
            return False
        else:
            return True


    def create_next_round(tournament: Tournament):
        players_sorted = sorted(tournament.players, key=lambda x: x['score'], reverse=True)
        i = 1
        while i < len(players_sorted):
            if players_sorted[i][('score')] == players_sorted[i - 1]['score']:
                if players_sorted[i]['elo'] < players_sorted[i - 1]['elo']:
                    players_sorted[i], players_sorted[i - 1] = players_sorted[i - 1], players_sorted[i]
                    i = 1
                    continue
            i += 1
        old_pairings = []
        for round in tournament.rounds:
            for game in round['games']:
                old_pairings.append([game[0][0], game[1][0]])
        
        new_pairing = []
        counter = len(players_sorted)
        while len(players_sorted) >= 2:
            p1 = players_sorted[0]
            i = 1
            if len(players_sorted) == 2:
                p2 = players_sorted[i]
                new_pairing.append([p1, p2])
                players_sorted.remove(p1)
                players_sorted.remove(p2)
                break
            while i < len(players_sorted):
                p2 = players_sorted[i]
                if p1 != p2 and [p1, p2] not in old_pairings and [p2, p1] not in old_pairings:
                    new_pairing.append([p1, p2])
                    players_sorted.remove(p1)
                    players_sorted.remove(p2)
                    break
                i += 1
            counter -= 1
            if counter == 0:
                return
        next_games = []
        for pair in new_pairing:
            p1 = [p for p in players_sorted if p == pair[0]]
            p2 = [p for p in players_sorted if p == pair[1]]
            next_games.append([[p1, 0], [p2, 0]])
        round = Round(
            name = 'Round {}'.format(len(tournament.rounds) + 1),
            games = next_games,
            start_date = datetime.today().strftime('%Y-%m-%d %H:%M')
        )


    def end_round(tournament: Tournament):
        end_date = datetime.today().strftime('%Y-%m-%d %H:%M')
        tournament.end_round_in_tournament_db(end_date)


    def update_selected_tournament(tournament):
        tournament_updated = Tournament.find_tournament(tournament)
        return Tournament.deserialize(tournament_updated)