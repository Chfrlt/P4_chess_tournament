class RoundView:

    def print_game(game_number: int, player1: dict, player2: dict, score1: int, score2: int):
        print(f"""| Game {game_number + 1} |
        {player1['surname']} {player1['first_name']}, score: {player1['score']}, elo: {player1['elo']}
        versus
        {player2['surname']} {player2['first_name']}, score: {player2['score']}, elo: {player2['elo']}""")
        if score1 > score2:
            print(f"Result: {player1['surname']} {player1['first_name']} WIN")
        elif score2 > score1:
            print(f"Result: {player2['surname']} {player2['first_name']} WIN")
        elif score1 == 0.5:
            print(f"Result: DRAW")


    def game_selector_view():
        return input('Game number ?\n >> ')


    def update_game_view(game_index: int, player1, player2):
        print('Edit results for Game {}: '.format(game_index + 1))
        print(' [1] player: {} {} win'.format(player1['surname'], player1['first_name']))
        print(' [2] player: {} {} win'.format(player2['surname'], player2['first_name']))
        print(' [3] Draw game')
        print(' [4] Reset results')
        print(' [0] Cancel')
        return input('Result ?\n >> ')