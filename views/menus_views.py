def main_menu_view(tournament):
    print('== Main Menu ==')
    if tournament is not None:
        print('Current tournament: {}, {}, {}, Date start: {}, Date end: {}'
            .format(tournament.name, tournament.location, tournament.game_format,
                tournament.date_start, tournament.date_end))
    print('[1] Create tournament')
    print('[2] Select tournament')
    print('[3] See tournament informations')
    print('[4] Tournament menu')
    print('[5] Player menu')
    print('[6] Delete all tournaments')
    print('[0] Exit')
    return input('>> Select: ')


def tournament_submenu_view(tournament, current_round: str):
    """Tournament menu"""
    print('== Tournament Menu ==')
    print('{}, {}, {}, {}, {}'
        .format(tournament.name, tournament.location, tournament.game_format,
            tournament.date_start, tournament.date_end))
    print('{}'.format(current_round))
    print('===================')
    print('[1] Show games in round')
    print('[2] Edit round')
    print('[3] End round')
    print('[4] Create Player')
    print('[5] Add Player')
    print("[6] Tournament's games history")
    print('[7] Start next round')
    print('[9] Main Menu')
    print('[0] Exit')
    return input('>> Select: ')


def player_submenu_view():
    print('== Player menu ==')
    print('===================')
    print('[1] Show all players')
    print('[2] Show all players by name')
    print('[3] Show all players by elo')
    print('[4] Show all players by score')
    print('[5] Create player(s)')
    print("[6] Update a player's elo")
    print('[7] Delete all players in database')
    print('[9] Main Menu')
    print('[0] Exit')
    return input('>> Select: ')


def screen(action, *arg):
    if isinstance(action, str):
        print(action)
        input('Press a key to continue.')
        return
    elif arg:
        return_value = action(arg)
    else:
        return_value = action()
    input('Success!\n Press a key to continue.')
    return return_value if return_value else None

def get_user_input(message):
    return input(message)