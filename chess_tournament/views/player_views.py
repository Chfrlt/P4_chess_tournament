from views.shared_view import (error_invalid_user_input,
                               get_input_for_selectors)


def creator_view() -> dict:
    parameters = {}
    parameters['first_name'] = input('First name ? [0] Cancel\n >> ')
    if parameters['first_name'] == str(0):
        return
    parameters['surname'] = input('Surname ?\n >> ')
    parameters['birthdate'] = input('birthdate ?\n >> ')
    parameters['gender'] = input('Gender ?\n >> ')
    parameters['elo'] = input('Elo ?\n >> ')
    return parameters


def player_selector_view(players_list: list) -> dict:
    for i, p in enumerate(players_list):
        print(f"[{i + 1}] {p}")
    max_index = len(players_list)
    while True:
        index = get_input_for_selectors(max_index)
        return index


def update_view(player: dict) -> dict:
    duplicate_p = {key: value for key, value in player.items() if key != 'score' and key != 'id'}
    keys = list(duplicate_p)
    for i, k in enumerate(duplicate_p):
        if k == 'id':
            continue
        if k == 'score':
            break
        else:
            print(f"[{i + 1}] {k}")
    print('[0] Cancel')
    print('Choose a value to update:')
    max_index = len(keys)
    while True:
        index = get_input_for_selectors(max_index)
        if index == -1 or index is None:
            break
        else:
            key_to_update = keys[index]
            old_value = player[key_to_update]
            print(f"Current value: {old_value}")
            new_value = input('New value: ')
            if new_value is None:
                error_invalid_user_input(error=ValueError)
            else:
                return {'key': key_to_update, 'value': new_value}


def print_players(players: list):
    for i, player in enumerate(players):
        print(f"[{i + 1}] | {player}")
    input('Press a key to continue.')


def invalid_elo_input():
    print("Invalid Elo Input: Player's elo must be a positive number.")
