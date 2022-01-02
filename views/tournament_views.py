from views.shared_view import SharedView


class TournamentView(SharedView):

    @staticmethod
    def creator_view() -> dict:
        parameters = {}
        parameters['name'] = input('Name ?\n >> ')
        parameters['location'] = input('Location ?\n >> ')
        format_options = ('rapid', 'blitz', 'bullet')
        max_index = len(format_options)
        print('Format ?\n    [1] rapid\n    [2] blitz\n    [3] bullet')
        while True:
            index = TournamentView.get_input_for_selectors(max_index)
            parameters['game_format'] = format_options[index]
            break
        parameters['description'] = input('Description ?\n >> ')
        parameters['date_start'] = input('Starting date ?\n >> ')
        print('Ending date ?')
        print('Optional | [0]: Same as starting date.')
        input_date_end = input(' >> ')
        if TournamentView.input_is_valid_as_an_int(input_date_end) is True:
            if int(input_date_end) == 0:
                parameters['date_end'] = parameters['date_start']
            else:
                parameters['date_end'] = input_date_end 
        else:
            parameters['date_end'] = input_date_end
        return parameters

    @staticmethod
    def print_tournaments(tournaments_strings: list) -> int:
        print('== Tournaments ==')
        for i, t in enumerate(tournaments_strings):
            print(f"[{i + 1}] {t}")

    @staticmethod
    def print_players(players_strings: list):
        print('== Players in Tournament ==')
        for i, p in enumerate(players_strings):
            print(f"[{i + 1}]: | {p}")
        input('Press a key to continue.')

    @staticmethod
    def no_players_error():
        print('No players found.')
        input('Press a key to continue')

    @staticmethod
    def no_tournaments_error():
        print('No tournaments found.')
        input('Press a key to continue')

    @staticmethod
    def get_input_for_selectors(max_index: int) -> int:
        '''takes user input, check if it is a valid and
        if it is inferior to the max index.

        If both conditions are met, returns the index'''
        raw_input = input(' >> ')
        if TournamentView.input_is_valid_as_an_int(raw_input) is True:
            index = int(raw_input) - 1
            if index > max_index:
                SharedView.error_invalid_user_input(error=IndexError)
            else:
                return index
