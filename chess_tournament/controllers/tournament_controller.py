from datetime import datetime

from models.player_model import Player
from models.tournament_model import Tournament
import views.tournament_views


class TournamentControl:

    def __init__(self) -> None:
        pass

    def tournament_selector(self) -> Tournament:
        tournaments_list = Tournament.get_tournaments_in_db()
        tournaments_strings = []
        for tournament in tournaments_list:
            tournaments_strings.append(repr(tournament))
        views.tournament_views.print_tournaments(tournaments_strings)
        max_index = len(tournaments_list)
        while True:
            index = views.tournament_views.get_input_for_selectors(max_index)
            if index is not None:
                if index > -1:
                    tournament = tournaments_list[index]
                    return tournament
                else:
                    views.tournament_views.error_invalid_user_input(
                        error=IndexError)

    def tournament_player_selector(self, tournament: Tournament) -> dict:
        players_list = tournament.players
        players_strings = []
        for player in players_list:
            player = Player.deserialize(player)
            players_strings.append(repr(player))
        views.tournament_views.print_players(players_strings)
        max_index = len(players_list)
        while True:
            index = views.tournament_views.get_input_for_selectors(max_index)
            if index is not None:
                player = players_list[index]
                return player

    def create_tournament(self) -> Tournament:
        tournament_parameters = views.tournament_views.creator_view()
        new_tournament = Tournament(
            tournament_parameters['name'],
            tournament_parameters['location'],
            tournament_parameters['game_format'],
            tournament_parameters['description'],
            tournament_parameters['date_start'],
            tournament_parameters['date_end'])
        Tournament.insert(new_tournament)
        return new_tournament

    def get_sorted_players_in_tournament(self, tournament: Tournament,
                                         score_sorted: bool = False,
                                         elo_sorted: bool = False,
                                         _print: bool = False) -> list:
        players = tournament.players
        if score_sorted is True:
            players = sorted(players, key=lambda x: x['score'], reverse=True)
        if elo_sorted is True:
            players = sorted(players, key=lambda x: x['elo'], reverse=True)
        if _print is True:
            players_strings = []
            for player in players:
                player_obj = Player.deserialize(player)
                players_strings.append(repr(player_obj))
            views.tournament_views.print_players(players_strings)
        return players

    def update_a_player_in_tournaments(self, player_to_update: Player,
                                       updated_player: dict,
                                       curr_tournament: Tournament = None):
        if curr_tournament:
            players = curr_tournament.players
            for player in players:
                if player_to_update.surname == player['surname']:
                    index = players.index(player)
                    players[index] = updated_player
                    curr_tournament.update()
        for tournament in Tournament.get_tournaments_in_db():
            players = tournament.players
            for player in players:
                if player_to_update.surname == player['surname']:
                    index = players.index(player)
                    players[index] = updated_player
                    tournament.update()

    def end_round(self, tournament: Tournament):
        end_date = datetime.today().strftime('%Y-%m-%d %H:%M')
        tournament.get_last_round()['end_date'] = end_date
        tournament.update()

    def check_if_player_is_in_any_tournament(self, player: Player) -> bool:
        for tour in Tournament.get_tournaments_in_db():
            if player.serialize() in tour.players:
                return True

    def delete_player_in_tournaments(self, player: dict,
                                     tournament: Tournament = None):
        if tournament is None:
            for tournament in Tournament.get_tournaments_in_db():
                if player in tournament.players:
                    if tournament.has_started() is True:
                        break
                    else:
                        tournament.players.remove(player)
                        tournament.update()
        elif player in tournament.players:
            tournament.players.remove(player)
            tournament.update()

    def delete_tournament(self, tournament: Tournament = None,
                          all_tournaments: bool = False):
        if all_tournaments is True:
            Tournament.delete_all_tournaments()
        else:
            tournament.delete_a_tournament()

    def check_if_any_tournament_in_db(self) -> bool:
        if Tournament.get_tournaments_in_db():
            return True
        else:
            return False
