from views.shared_view import (input_is_valid_as_an_int,
                               get_input_for_selectors)


def creator_view() -> dict:
    parameters = {}
    parameters['name'] = input('Name ?\n >> ')
    parameters['location'] = input('Location ?\n >> ')
    format_options = ('rapid', 'blitz', 'bullet')
    max_index = len(format_options)
    print('Format ?\n    [1] rapid\n    [2] blitz\n    [3] bullet')
    while True:
        index = get_input_for_selectors(max_index)
        parameters['game_format'] = format_options[index]
        break
    parameters['description'] = input('Description ?\n >> ')
    parameters['date_start'] = input('Starting date ?\n >> ')
    print('Ending date ?')
    print('Optional | [0]: Same as starting date.')
    input_date_end = input(' >> ')
    if input_is_valid_as_an_int(input_date_end) is True:
        if int(input_date_end) == 0:
            parameters['date_end'] = parameters['date_start']
        else:
            parameters['date_end'] = input_date_end
    else:
        parameters['date_end'] = input_date_end
    return parameters


def tournament_selector_view(tournament_list: list) -> int:
    print('Select a tournament:\n [0] Cancel')
    for i, t in enumerate(tournament_list):
        print(f"[{i + 1}] {t}")
    max_index = len(tournament_list)
    while True:
        index = get_input_for_selectors(max_index)
        return index


def print_tournaments(tournaments_strings: list) -> int:
    print('== Tournaments ==')
    for i, t in enumerate(tournaments_strings):
        print(f"[{i + 1}] {t}")


def print_players(players_strings: list):
    print('== Players in Tournament ==')
    for i, p in enumerate(players_strings):
        print(f"[{i + 1}]: | {p}")
    input('Press a key to continue.')


def no_players_error():
    print('No players found.')
    input('Press a key to continue')


def no_tournaments_error():
    print('No tournaments found.')
    input('Press a key to continue')
