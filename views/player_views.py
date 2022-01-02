class PlayerView:


    def creator_view():
        parameters = {}
        parameters['first_name'] = input('First name ?')
        parameters['surname'] = input('surname ?')
        parameters['birthdate'] = input('birthdate ?')
        parameters['gender'] = input('Gender ?')
        parameters['elo'] = input('Elo ?')
        return parameters


    def selector_view(list_ = None):
        if list_ is None:
            print('No players')
        else:
            for i, p in enumerate(list_):
                print("[{}] {}".format(i + 1, p))
                print('>> Select Player: ')


    def update_view(param: str):
        print('Enter new {}:'.format(param))


    def print_players_unsorted(players: list):
        for player in players:
            print(f"Name: {player.surname} {player.first_name}, birthdate: {player.birthdate}, gender: {player.gender}, elo: {player.elo}")


    def print_players_name_sorted(list_players_name_sorted: list):
        print('= Players by name =')
        for player in list_players_name_sorted:
            print(
                f"Name: {player.surname} {player.first_name}, birthdate: {player.birthdate}, gender: {player.gender}, elo: {player.elo}"
                )


    def print_players_elo_sorted(list_players_elo_sorted: list):
        print('= Players by elo =')
        for player in list_players_elo_sorted:
            print(
                f"Name: {player.surname} {player.first_name}, birthdate: {player.birthdate}, gender: {player.gender}, elo: {player.elo}"
                )


    def print_players_score_sorted(list_players_score_sorted: list):
        print('= Players by score =')
        for player in list_players_score_sorted:
            print(
                f"Name: {player.surname} {player.first_name}, birthdate: {player.birthdate}, gender: {player.gender}, elo: {player.elo}"
                )


    def print_individual_player(player: object):
        print(
                'name: {} {}, birthdate: {}, gender: {}, elo: }'
                .format(player.surname, player.first_name, player.birthdate, player.gender, player.elo)
                )