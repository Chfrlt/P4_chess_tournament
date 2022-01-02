import sys

from views.menus_views import MenuView
from controllers.round_controller import RoundControl
from controllers.player_controller import PlayerControl
from controllers.tournament_controller import TournamentControl


class MenuControl():

    def __init__(self, player_controller: PlayerControl,
                 tournament_controller: TournamentControl,
                 round_controller: RoundControl):

        self.options = {}
        self.tournament = None
        self.name = None
        self.p_control = player_controller
        self.t_control = tournament_controller
        self.r_control = round_controller

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
        options_list = list(self.options)

        while True:
            tour_str = repr(self.tournament) if self.tournament else None
            action = MenuView.menu_view(options_list, self.name,
                                        tour_str)
            if action in self.options:
                self.execute_action(action)

    def tournament_menu(self):
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
        options_list = list(self.options)

        while True:
            if self.tournament is None:
                MenuView.error_no_tournament_selected()
                self.main_menu()
            tour_str = (
                repr(self.tournament) if self.tournament else None)
            if self.tournament.has_started():
                rnd_str = repr(self.tournament.get_last_round())
            else:
                rnd_str = None
            action = MenuView.menu_view(options_list, self.name,
                                        tour_str, rnd_str)
            if action:
                self.execute_action(action)

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
        options_list = list(self.options)

        while True:
            tour_str = repr(self.tournament) if self.tournament else None
            action = MenuView.menu_view(options_list, self.name, tour_str)
            if action:
                self.execute_action(action)

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
        options_list = list(self.options)

        while True:
            tour_str = repr(self.tournament) if self.tournament else None
            action = MenuView.menu_view(options_list, self.name, tour_str)
            self.execute_action(action)

    def create_tournament(self):
        if not self.tournament:
            self.tournament = self.t_control.create_tournament()
        else:
            self.t_control.create_tournament()

    def select_tournament(self):
        if self.t_control.check_if_tournament_in_db() is True:
            self.tournament = self.t_control.tournament_selector()
        else:
            MenuView.error_no_tournament_in_db()

    def delete_tournament(self):
        confirmation = MenuView.delete_all_tournament_input_confirmation()
        if confirmation == 'y':
            self.t_control.delete_tournament(all_tournaments=True)
            MenuView.delete_all_tournament_success()
            self.tournament = None
        else:
            tournament_to_delete = self.t_control.tournament_selector()
            if self.tournament:
                if self.tournament.name == tournament_to_delete.name:
                    self.tournament = None
            self.t_control.delete_tournament(tournament_to_delete)

    def show_games_in_round(self):
        if self.tournament.has_started() is True:
            self.r_control.display_round_infos(
                self.tournament.get_last_round(), print_games=True)
        elif not self.tournament.has_started() is False:
            MenuView.error_tournament_not_started()

    def edit_game(self):
        if self.tournament.has_started() is True:
            if self.tournament.get_last_round().has_ended() is True:
                rnd_modif_confirmation = (
                    MenuView.round_modification_input_confirmation())
                if rnd_modif_confirmation != 'y':
                    return
            game_selection = (
                self.r_control.selector_game(self.tournament.get_last_round())
                )
            if game_selection is not None:
                self.r_control.update_game(game_selection, self.tournament)
        else:
            MenuView.error_tournament_not_started()

    def start_next_round(self):
        if self.tournament.is_full() is True:
            if self.tournament.has_started() is True:
                if self.tournament.get_last_round().has_ended() is True:
                    if self.tournament.has_ended() is True:
                        "print smth"
                    else:
                        self.r_control.create_round(self.tournament)
                else:
                    MenuView.error_round_not_ended()
            else:
                self.r_control.create_round(self.tournament)
        else:
            MenuView.error_tournament_not_full()

    def end_round(self):
        if self.tournament.has_started() is False:
            MenuView.error_tournament_not_started()
        elif self.tournament.has_started() is True:
            current_round = self.tournament.get_last_round()
            if self.tournament.has_ended() is True:
                MenuView.error_tournament_ended()
                self.show_player_in_tournament_by_score()
            while current_round.is_completed() is False:
                    for index in current_round.get_indexes_non_completed_games():
                        self.r_control.update_game(index, self.tournament)
                        RoundControl.end_round(self.tournament)
            else:
                RoundControl.end_round(self.tournament)

    def get_tournament_games_history(self):
        for round in self.tournament.get_rounds():
            self.r_control.display_round_infos(round, print_games=True)

    def show_all_players(self):
        self.p_control.show_players_in_db()

    def show_all_players_by_name(self):
        self.p_control.show_players_in_db(name_sorted=True)

    def show_all_players_by_elo(self):
        self.p_control.show_players_in_db(elo_sorted=True)

    def create_players(self):
        option_add_to_tournament = None
        while True:
            to_create_str = MenuView.get_input_nbr_players_to_create()
            try:
                number_to_create = int(to_create_str)
                break
            except ValueError as e:
                MenuView.error_invalid_user_input(e)
        if number_to_create == 0:
            return
        if self.tournament:
            if number_to_create + self.tournament.player_count() <= 8:
                option_add_to_tournament = (
                    MenuView.option_add_to_tournament_when_player_creation())
        for n in range(number_to_create):
            MenuView.player_creation_number_printer(n + 1)
            new_player = self.p_control.create_player()
            if option_add_to_tournament == 'y':
                self.tournament.add_player_to_tournament(new_player)

    def update_players(self):
        player_to_update = self.p_control.selector()
        if player_to_update is None:
            return
        updated_player = self.p_control.update_player(player_to_update)
        if updated_player is None:
            return
        self.t_control.update_a_player_in_tournaments(player_to_update,
                                                      updated_player,
                                                      self.tournament)

    def delete_players_db(self):
        option_all_players_deletion = (
            MenuView.delete_all_players_input_confirmation())
        if option_all_players_deletion == 'y':
            self.p_control.delete_player(all=True)
        else:
            player_to_delete = self.p_control.selector()
            if self.t_control.check_if_player_is_in_any_tournament(
                    player_to_delete) is True:
                delete_confirmation = (
                    MenuView.error_player_deletion_exist_in_tournament())
                if delete_confirmation != 'y':
                    return
                else:
                    self.t_control.delete_player_in_tournaments(
                        player_to_delete.serialize())
                    self.p_control.delete_player(player=player_to_delete)
            else:
                self.p_control.delete_player(player=player_to_delete)

    def add_player_to_tournament(self):
        if self.tournament.player_count() == 8:
            MenuView.error_tournament_is_full()
        elif self.p_control.check_if_player_in_db() is False:
            MenuView.error_no_player_in_db()
        else:
            player = self.p_control.selector()
            if player is not None:
                if player.serialize() in self.tournament.players:
                    MenuView.error_player_already_in_tournament()
                else:
                    self.tournament.add_player_to_tournament(player)
                    MenuView.player_add_to_tournament_success(player.surname,
                                                              player.first_name)

    def show_player_in_tournament_by_score(self):
        if not self.tournament.players:
            MenuView.error_no_players_in_tournament()
        else:
            TournamentControl.get_sorted_players_in_tournament(
                self.tournament, score_sorted=True, _print=True)

    def show_player_in_tournament(self):
        if not self.tournament.players:
            MenuView.error_no_players_in_tournament()
        else:
            TournamentControl.get_sorted_players_in_tournament(
                self.tournament, elo_sorted=True, _print=True)

    def delete_player_in_tournament(self):
        if self.tournament.has_started() is True:
            MenuView.error_tournament_started()
        else:
            player_to_delete = (
                self.t_control.tournament_player_selector(self.tournament))
            self.t_control.delete_player_in_tournaments(
                player_to_delete, self.tournament)

    def execute_action(self, action):
        if action:
            if action in self.options:
                self.options[action]()
