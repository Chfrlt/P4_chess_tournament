from typing import Any
from views.shared_view import SharedView


class PlayerView(SharedView):

    @staticmethod
    def creator_view():
        parameters = {}
        parameters['first_name'] = input('First name ?\n >> ')
        parameters['surname'] = input('Surname ?\n >> ')
        parameters['birthdate'] = input('birthdate ?\n >> ')
        parameters['gender'] = input('Gender ?\n >> ')
        parameters['elo'] = input('Elo ?\n >> ')
        return parameters

    @staticmethod
    def selector_view(players_list: list) -> dict:
        for i, p in enumerate(players_list):
            print(f"[{i + 1}] {p}")
        max_index = len(players_list)
        while True:
            index = PlayerView.get_input_for_selectors(max_index)
            return index

    @staticmethod
    def update_view(player: dict) -> dict:
        keys = list(player)
        for i, k in enumerate(player):
            if k == 'score':
                break
            print(f"[{i + 1}] {k}")
        print('[0] Cancel')
        print('Choose a value to update:')
        max_index = len(keys)
        while True:
            index = PlayerView.get_input_for_selectors(max_index)
            if index == -1 or index is None:
                break
            else:
                key_to_update = keys[index]
                old_value = player[key_to_update]
                print(f"Current value: {old_value}")
                new_value = input('New value: ')
                if new_value is None:
                    PlayerView.error_invalid_user_input(error=ValueError)
                else:
                    return {'key': key_to_update, 'value': new_value}

    @staticmethod
    def print_players(players_strings: list):
        for i, player in enumerate(players_strings):
            print(f"[{i + 1}] | {player}")
        input('Press a key to continue.')

    @staticmethod
    def invalid_elo_input():
        print("Invalid Elo Input: Player's elo must be a positive number.")

