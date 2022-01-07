from views.shared_view import get_input_for_selectors


def print_round(round_repr: str):
    print(round_repr)


def print_game(games_reprs: str):
    for game in games_reprs:
        print(game)
    input('Press a key to continue')


def game_selector_view() -> int:
    print('Select a game:\n [0] Cancel')
    while True:
        game_selection = get_input_for_selectors(4)
        if game_selection == -1:
            break
        else:
            return game_selection


def update_game_view(game_index: int, player1, player2) -> int:
    print(f"Edit results for Game {game_index + 1}: ")
    print(f"[1] player: {player1['surname']} {player1['first_name']} win")
    print(f"[2] player: {player2['surname']} {player2['first_name']} win")
    print('[3] Draw game')
    print('[4] Reset results')
    print('[0] Cancel')
    print('Result ?')
    while True:
        result_input = get_input_for_selectors(4)
        return result_input
