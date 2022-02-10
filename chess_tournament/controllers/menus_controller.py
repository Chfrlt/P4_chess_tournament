import sys

import views.menus_views
from controllers.round_controller import RoundControl
from controllers.player_controller import PlayerControl
from controllers.tournament_controller import TournamentControl


class MenuControl(RoundControl, PlayerControl, TournamentControl):

    def __init__(self):
        super().__init__()
        self.options = {}
        self.tournament = None
        self.name = None

    def execute_menu(self):
        while True:
            tour = self.tournament
            rnd = (self.tournament.get_last_round()
                   if self.tournament and self.tournament.has_started() is True else None)
            options_list = list(self.options)
            action = views.menus_views.menu_view(options_list, self.name,
                                                 tour, rnd)
            if action in self.options:
                self.execute_action(action)

    def execute_action(self, action):
        if action:
            if action in self.options:
                self.options[action]()

    def main_menu(self):
        self.name = 'Main Menu'
        self.options = {
            'Create tournament': self.create_tournament,
            'Select tournament': self.select_tournament,
            'Tournament menu': self.tournament_menu,
            'Player menu': self.player_menu,
            'Delete tournament(s)': self.delete_tournament,
            'Exit': sys.exit
            }

    def tournament_menu(self):
        if self.tournament is None:
            views.menus_views.error_no_tournament_selected()
            return
        self.name = 'Tournament Menu'
        self.options = {
            'Show games in round': self.show_games_in_round,
            'Edit a game in round': self.edit_game,
            'Start next round': self.start_next_round,
            'End round': self.end_round,
            "Tournament's games history": self.get_tournament_games_history,
            'Player management': self.player_management_menu,
            'Main menu': self.main_menu,
            'Exit': sys.exit
            }

    def player_menu(self):
        self.name = 'Player Menu'
        self.options = {
            'Show all players': self.show_all_players,
            'Show all players by name': self.show_all_players_by_name,
            'Show all players by elo': self.show_all_players_by_elo,
            'Create player(s)': self.create_players,
            'Update a player': self.update_players,
            'Delete player(s) in database': self.delete_players_db,
            'Main menu': self.main_menu,
            'Exit': sys.exit
            }

    def player_management_menu(self):
        self.name = 'Player Management'
        self.options = {
            "Create player(s)": self.create_players,
            'Add Player to tournament': self.add_player_to_tournament,
            'Show players in tournament': self.show_player_in_tournament,
            'Show players in tournament by score':
                self.show_player_in_tournament_by_score,
            'Delete a player in tournament': self.delete_player_in_tournament,
            'Tournament menu': self.tournament_menu,
            'Main menu': self.main_menu,
            'Exit': sys.exit
            }

    def create_tournament(self):
        if not self.tournament:
            self.tournament = super().create_tournament()
        else:
            super().create_tournament()

    def select_tournament(self):
        if self.check_if_any_tournament_in_db() is True:
            self.tournament = super().tournament_selector()
        else:
            views.menus_views.error_no_tournament_in_db()

    def delete_tournament(self):
        confirmation = (
            views.menus_views.delete_all_tournament_input_confirmation())
        if confirmation == 'y':
            super().delete_tournament(self.tournament, all_tournaments=True)
            views.menus_views.delete_all_tournament_success()
            self.tournament = None
        else:
            tournament_to_delete = super().tournament_selector()
            if self.tournament:
                if self.tournament.name == tournament_to_delete.name:
                    self.tournament = None
            super().delete_tournament(tournament_to_delete)

    def show_games_in_round(self):
        if self.tournament.has_started() is True:
            self.display_round_infos(
                self.tournament.get_last_round(), print_games=True)
        elif self.tournament.has_started() is False:
            views.menus_views.error_tournament_not_started()

    def edit_game(self):
        if self.tournament.has_started() is True:
            if self.tournament.get_last_round().has_ended() is True:
                rnd_modif_confirmation = (
                    views.menus_views.round_modification_input_confirmation())
                if rnd_modif_confirmation != 'y':
                    return
            game_selection = (
                super().selector_game(self.tournament.get_last_round())
                )
            if game_selection is not None:
                self.update_game(game_selection, self.tournament)
        else:
            views.menus_views.error_tournament_not_started()

    def start_next_round(self):
        if self.tournament.is_full() is True:
            if self.tournament.has_started() is True:
                if self.tournament.get_last_round().has_ended() is True:
                    if self.tournament.has_ended() is True:
                        views.menus_views.error_tournament_ended()
                        self.show_player_in_tournament_by_score()
                    else:
                        self.create_round(self.tournament)
                else:
                    views.menus_views.error_round_not_ended()
            else:
                self.create_round(self.tournament)
        else:
            views.menus_views.error_tournament_not_full()

    def end_round(self):
        if self.tournament.has_started() is False:
            views.menus_views.error_tournament_not_started()
        elif self.tournament.has_started() is True:
            current_round = self.tournament.get_last_round()
            if self.tournament.has_ended() is True:
                views.menus_views.error_tournament_ended()
                self.show_player_in_tournament_by_score()
            while current_round.is_completed() is False:
                for index in current_round.get_indexes_non_completed_games():
                    self.update_game(index, self.tournament)
                    super().end_round(self.tournament)
            else:
                super().end_round(self.tournament)

    def get_tournament_games_history(self):
        if self.tournament.has_started():
            for round in self.tournament.get_rounds():
                self.display_round_infos(round, print_games=True)
        else:
            views.menus_views.error_tournament_not_started()

    def show_all_players(self):
        if self.check_if_player_in_db() is False:
            views.menus_views.error_no_player_in_db()
        else:
            super().show_players_in_db()

    def show_all_players_by_name(self):
        if self.check_if_player_in_db() is False:
            views.menus_views.error_no_player_in_db()
        else:
            super().show_players_in_db(name_sorted=True)

    def show_all_players_by_elo(self):
        if self.check_if_player_in_db() is False:
            views.menus_views.error_no_player_in_db()
        else:
            super().show_players_in_db(elo_sorted=True)

    def create_players(self):
        option_add_to_tournament = None
        while True:
            to_create_str = views.menus_views.get_input_nbr_players_to_create()
            try:
                number_to_create = int(to_create_str)
                break
            except ValueError as e:
                views.menus_views.error_invalid_user_input(e)
        if number_to_create == 0:
            return
        if self.tournament:
            if number_to_create + self.tournament.player_count() <= 8:
                option_add_to_tournament = (
                    views.menus_views
                    .option_add_to_tournament_when_player_creation())
        for n in range(number_to_create):
            views.menus_views.player_creation_number_printer(n + 1)
            new_player = super().create_player()
            if option_add_to_tournament == 'y':
                self.tournament.add_player_to_tournament(new_player)

    def update_players(self):
        player_to_update = super().player_selector()
        if player_to_update is None:
            return
        updated_player = super().update_player(player_to_update)
        if updated_player is None:
            return
        super().update_a_player_in_tournaments(player_to_update,
                                               updated_player,
                                               self.tournament)

    def delete_players_db(self):
        option_all_players_deletion = (
            views.menus_views.delete_all_players_input_confirmation())
        if option_all_players_deletion == 'y':
            super().delete_player(all=True)
        else:
            player_to_delete = super().player_selector()
            if self.check_if_player_is_in_any_tournament(
                    player_to_delete) is True:
                delete_confirmation = (
                    views.menus_views
                    .error_player_deletion_exist_in_tournament())
                if delete_confirmation != 'y':
                    return
                else:
                    super().delete_player_in_tournaments(
                        player_to_delete.serialize())
                    super().delete_player(player=player_to_delete)
            else:
                super().delete_player(player=player_to_delete)

    def add_player_to_tournament(self):
        if self.tournament.player_count() == 8:
            views.menus_views.error_tournament_is_full()
        elif self.check_if_player_in_db() is False:
            views.menus_views.error_no_player_in_db()
        else:
            player = super().player_selector()
            if player is not None:
                if player.serialize() in self.tournament.players:
                    views.menus_views.error_player_already_in_tournament()
                else:
                    self.tournament.add_player_to_tournament(player)
                    views.menus_views.player_add_to_tournament_success(
                        player.surname,
                        player.first_name)

    def show_player_in_tournament_by_score(self):
        if not self.tournament.players:
            views.menus_views.error_no_players_in_tournament()
        else:
            super().get_sorted_players_in_tournament(
                self.tournament, score_sorted=True, _print=True)

    def show_player_in_tournament(self):
        if not self.tournament.players:
            views.menus_views.error_no_players_in_tournament()
        else:
            super().get_sorted_players_in_tournament(
                self.tournament, elo_sorted=True, _print=True)

    def delete_player_in_tournament(self):
        if self.tournament.has_started() is True:
            views.menus_views.error_tournament_started()
        else:
            player_to_delete = (
                super().tournament_player_selector(self.tournament))
            super().delete_player_in_tournaments(
                player_to_delete, self.tournament)
