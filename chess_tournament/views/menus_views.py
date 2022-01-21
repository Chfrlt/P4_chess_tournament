from typing import Union

import views.shared_view


def menu_view(options: list, name: str,
              tournament: object = None,
              round: object = None):
    print(f"== {name} ==")
    print('==============')
    if tournament:
        print('Selected Tournament:')
        print(tournament)
        if round:
            print(round)
        print('==============')
    for i, o in enumerate(options):
        print(f"[{i + 1}] {o}")
    index = views.shared_view.get_input_for_selectors(i)
    if index is not None:
        if index == -1:
            return
        option_selected = options[index]
        print(option_selected)
        return option_selected


def input_validation(raw_input: str,
                     options: list) -> Union[ValueError, IndexError, str]:
    try:
        user_input = int(raw_input)
        option_selected = options[user_input - 1]
        return option_selected
    except ValueError as e:
        error_invalid_user_input(e)
        return
    except IndexError as e:
        error_invalid_user_input(e)
        return


def error_invalid_user_input(error: Union[ValueError, IndexError]):
    if isinstance(error, ValueError):
        print('Invalid Input. Must be a number')
    elif isinstance(error, IndexError):
        print("Input didn't match any options")


def error_no_tournament_selected():
    print('No tournament selected. '
          'Please select a tournament first.')
    input('Press a key to continue.')


def error_tournament_not_started():
    print("Tournament hasn't started. "
          'Start tournament by creating a round.')
    input('Press a key to continue.')


def error_tournament_started():
    print('Tournament has started. Option is no longer available.')
    input('Press a key to continue.')


def delete_all_tournament_input_confirmation() -> str:
    print('Delete all tournaments ? | y/n')
    return input(' >> ')


def delete_all_tournament_success():
    print('All tournaments have been deleted.')
    input('Press a key to continue.')


def delete_all_players_input_confirmation() -> str:
    print('Delete all players ? | y/n')
    return input(' >> ')


def delete_all_players_success():
    print('All players have been deleted.')
    input('Press a key to continue.')


def error_player_deletion_exist_in_tournament() -> str:
    print('Player exist in one or more existing tournament(s).'
          ' Proceeding will delete the player from tournament(s)'
          ' whom have not started.')
    print('Do you still wish to continue ? | y/n')
    return input(' >> ')


def round_modification_input_confirmation() -> str:
    print('Round has ended. Do you still wish to proceed ?  | y/n')
    return input(' >> ')


def error_round_not_ended():
    print('End the current round first.')
    input('Press a key to continue.')


def error_tournament_not_full():
    print('Tournament requires 8 registered players to start round.')
    input('Press a key to continue.')


def error_tournament_is_full():
    print('The maximum number of players (8) has been reached')
    input('Press a key to continue.')


def get_input_nbr_players_to_create() -> str:
    print('Number of players to create:')
    print('[0] Cancel')
    return input(' >> ')


def option_add_to_tournament_when_player_creation() -> str:
    print('Do you wish to add the created players '
          'to the current tournament ? | y/n')
    return input(' >> ')


def error_no_player_in_db():
    print('No players in database. Please create player(s) first.')
    input('Press a key to continue.')


def error_no_tournament_in_db():
    print('No tournament in database. Please create a tournament first.')
    input('Press a key to continue.')


def error_no_players_in_tournament():
    print('No players in tournament.')
    input('Press a key to continue.')


def player_add_to_tournament_success(player_surname, player_first_name):
    print(f"{player_surname} {player_first_name} succesfully "
          'added to the tournament.')
    input('Press a key to continue.')


def error_round_already_ended():
    print('Round has already ended. '
          'You can still edit games using the "edit games" options.')
    print('If you wish to proceed to next round, '
          'use the "start next round" option.')
    input('Press a key to continue')


def error_tournament_ended():
    print('The 4 round have been played, tournament has ended.')
    print('==== Results ====')


def player_creation_number_printer(player_number: int):
    print(f"== Creating Player {player_number} ==")


def error_player_already_in_tournament():
    print('Impossible: Selected player is already in tournament')
    input('Press a key ton continue.')
