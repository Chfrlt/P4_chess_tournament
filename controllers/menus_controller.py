import sys

from controllers.round_controller import RoundControl
from controllers.player_controller import PlayerControl
from controllers.tournament_controller import TournamentControl
from views.menus_views import *
from models.player_model import Player
from models.tournament_model import Tournament


SELECTED_TOURNAMENT = None


def main_menu():
    '''[1] Create Tournament [2] Select Tournament [3] See Tournament Informations
    [4] Tournament menu [5] Player menu [0] Exit '''
    while True:
        global SELECTED_TOURNAMENT
        if SELECTED_TOURNAMENT is not None:
            SELECTED_TOURNAMENT = TournamentControl.update_selected_tournament(SELECTED_TOURNAMENT)

        selection = main_menu_view(SELECTED_TOURNAMENT)
        try:
            action = int(selection)
            if action > 0 and action < 5:
                if action == 1:
                    screen(TournamentControl.create_tournament)
                elif action == 2:
                    if Tournament.get_tournaments_in_db() is None:
                        screen('No tournament(s) in database. Please create a tournament first.')
                    else:
                        SELECTED_TOURNAMENT = TournamentControl.selector()
                elif action == 3:
                    if SELECTED_TOURNAMENT is None:
                        screen('No tournament selected. Please select a tournament first.')
                    else:
                        screen(SELECTED_TOURNAMENT.__repr__())
                elif action == 4:
                    if SELECTED_TOURNAMENT is None:
                        screen('No tournament selected. Please select a tournament first.')
                    else:
                        tournament_submenu()
            elif action == 5:
                player_submenu()
            elif action == 6:
                screen(Tournament.delete_all_tournaments)
            elif action == 0:
                sys.exit()
            else:
               continue
        except ValueError:
            continue


def tournament_submenu():
    '''Tournament menu
    [1] Show games in round
    [2] Enter a game result
    [3] End round
    [4] Create Player
    [5] Add player to current tournament
    [6] Tournament's games history
    [7] Start next round
    [9] Main Menu
    [0] Exit'''
    while True:
        global SELECTED_TOURNAMENT
        if SELECTED_TOURNAMENT is not None:
            SELECTED_TOURNAMENT = TournamentControl.update_selected_tournament(SELECTED_TOURNAMENT)

        if SELECTED_TOURNAMENT.rounds:
            round_current = (
                '{}, started: {}, end: {}'
                .format(SELECTED_TOURNAMENT.rounds[-1]['name'], 
                SELECTED_TOURNAMENT.rounds[-1]['start_date'], 
                (SELECTED_TOURNAMENT.rounds[-1]['end_date']
                    if SELECTED_TOURNAMENT.rounds[-1]['end_date'] != '' else 'In progress'))
                )
        else:
            round_current = "Tournament didn't start"
        selection = tournament_submenu_view(SELECTED_TOURNAMENT, round_current)
        try:
            action = int(selection)
            if action > 0 and action < 8:
                if action == 1:
                    if SELECTED_TOURNAMENT.rounds:
                        RoundControl.show_games(SELECTED_TOURNAMENT)
                        screen('')
                    else:
                        screen("Tournament didn't start")
                elif action == 2:
                    if SELECTED_TOURNAMENT.rounds:
                        game_selection = RoundControl.selector_game(SELECTED_TOURNAMENT)
                        RoundControl.update_game(game_selection, SELECTED_TOURNAMENT)
                    else:
                        screen("Tournament didn't start")
                elif action == 3:
                    TournamentControl.end_round(SELECTED_TOURNAMENT)
                elif action == 4:
                    input_number = get_user_input('Number of players to create:\n [0] Cancel\n >> ')
                    try:
                        number_to_create = int(input_number)
                        if number_to_create == 0:
                            break
                        if number_to_create < 9 and SELECTED_TOURNAMENT is not None:
                            option_add_to_tournament = get_user_input('Add created players to current tournament ?\n y/n\n')
                        for p in range(number_to_create):
                            new_player = PlayerControl.create_player()
                            if option_add_to_tournament and option_add_to_tournament == 'y':
                                TournamentControl.add_player_to_tournament(new_player, SELECTED_TOURNAMENT)
                    except ValueError:
                        continue
                elif action == 5:
                    if TournamentControl.check_if_tournament_is_full(SELECTED_TOURNAMENT):
                            screen(
                                'The maximum number of players (8) in tournament has been reached')
                    elif Player.get_players_in_db():
                            player = PlayerControl.selector()
                            TournamentControl.add_player_to_tournament(player, SELECTED_TOURNAMENT)
                            screen('{} {} succesfully added to the tournament'
                                .format(player.surname, player.first_name))
                    else:
                        screen('No players in database')
                elif action == 6:
                    'pass'
                elif action == 7:
                    if (SELECTED_TOURNAMENT.players and
                    TournamentControl.check_if_tournament_is_full(SELECTED_TOURNAMENT) is True):
                        if not SELECTED_TOURNAMENT.rounds:
                            RoundControl.create_first_round(SELECTED_TOURNAMENT)
                        elif SELECTED_TOURNAMENT.rounds[-1]['end_date'] is not None:
                            TournamentControl.create_next_round(SELECTED_TOURNAMENT)
                        else:
                            screen('End the current round first.')
                    else:
                        screen('Tournament requires 8 registered players to start round.')
            elif action == 9:
                main_menu()
            elif action == 0:
                sys.exit()
            else:
               continue
        except ValueError:
            continue


def player_submenu():
    '''Player menu
    [1] Show all players
    [2] Show all players by name
    [3] Show all players by elo
    [4] Show all players by score
    [5] Create player(s)
    [6] Update a player's elo
    [7] Delete all players in database
    [9] Main Menu
    [0] Exit'''
    global SELECTED_TOURNAMENT
    if SELECTED_TOURNAMENT is not None:
        SELECTED_TOURNAMENT = TournamentControl.update_selected_tournament(SELECTED_TOURNAMENT)
    
    while True:
        selection = player_submenu_view()
        try:
            action = int(selection)
            if action > 0 and action < 8:
                if action == 1:
                    screen(PlayerControl.show_players_unsorted)
                elif action == 2:
                    screen(PlayerControl.show_players_name_sorted)
                elif action == 3:
                    screen(PlayerControl.show_players_elo_sorted)
                elif action == 4:
                    screen(PlayerControl.show_players_score_sorted)
                elif action == 5:
                    input_number = get_user_input('Number of players to create:\n [0] Cancel\n >> ')
                    try:
                        number = int(input_number)
                        if number == 0:
                            break
                        if number < 9 and SELECTED_TOURNAMENT is not None:
                            option_add_to_tournament = get_user_input('Add created players to current tournament ?\n y/n\n')
                        new_players = PlayerControl.create_player(number)
                        if option_add_to_tournament and option_add_to_tournament == 'y':
                            TournamentControl.add_player_to_tournament(new_players, SELECTED_TOURNAMENT)
                    except ValueError:
                        continue
                elif action == 6:
                    PlayerControl.update_elo()
                elif action == 7:
                    Player.delete_all_players()
            elif action == 9:
                main_menu()
            elif action == 0:
                sys.exit()
            else:
                continue
        except ValueError:
            continue


main_menu()