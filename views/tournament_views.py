class TournamentView:
    def creator_view() -> dict:
        parameters = {}
        parameters['name'] = input("Name ? ")
        parameters['location'] = input("Location ? ")
        format_ref = ["rapid", "blitz", "bullet"]
        format_input = input("Format ?\n    1: rapid\n    2: blitz\n    3: bullet")
        try:
            index = int(format_input)
            parameters['game_format'] = format_ref[index]
        except ValueError or IndexError:
            print('Invalid input')
        except IndexError:
            print()
        parameters['description'] = input("Description ? ")
        parameters['date_start'] = input("Starting date ? ")
        parameters['date_end'] = input("Ending date ?\n Optional, [0]: Same as starting date.")
        return parameters


    def selector_view(tournaments):
        if type(tournaments) is list:
            for i, t in enumerate(tournaments):
                print('[{}] {}'.format(i + 1, t.__repr__()))
        print('>> Select: ')


    def start_tournament_view(self, tournament):
        print('Tournament started at {}'.format(tournament.rounds[0].start))


    def next_games_view(games_list):
        for game in games_list:
            print(game)


    def print_message(message):
        print(message)