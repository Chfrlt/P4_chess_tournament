from models.player_model import Player
import views.player_views


class PlayerControl:

    def __init__(self) -> None:
        pass

    def create_player(self) -> Player:
        while True:
            player_parameters = views.player_views.creator_view()
            if player_parameters:
                try:
                    new_player = Player(
                        len(Player.get_players_in_db())
                        if self.check_if_player_in_db() is True else 0,
                        player_parameters['first_name'],
                        player_parameters['surname'],
                        player_parameters['birthdate'],
                        player_parameters['gender'],
                        player_parameters['elo']
                    )
                    new_player.insert()
                    return new_player
                except ValueError:
                    views.player_views.invalid_elo_input()
            else:
                return

    def player_selector(self) -> Player:
        player_list = Player.get_players_in_db()
        index = views.player_views.player_selector_view(player_list)
        if index is not None:
            return player_list[index]

    def show_players_in_db(self, name_sorted=False, elo_sorted=False):
        if self.check_if_player_in_db() is True:
            players = Player.get_players_in_db()
            if name_sorted is True:
                players = sorted(players, key=lambda x: x.surname)
            elif elo_sorted is True:
                players = sorted(players, key=lambda x: x.elo, reverse=True)
            views.player_views.print_players(players)

    def update_player(self, player: Player) -> Player:
        player = player.serialize()
        to_update = views.player_views.update_view(player)
        if to_update is None:
            return
        new_value = to_update['value']
        key = to_update['key']
        if key == 'elo':
            try:
                new_value = Player.is_valid_elo(new_value)
            except ValueError:
                views.player_views.invalid_elo_input()
                return
        player[key] = new_value
        Player.deserialize(player).update_player_in_db()
        return player

    def check_if_player_in_db(self) -> bool:
        if Player.get_players_in_db():
            return True
        else:
            return False

    def delete_player(self, player: Player = None, all: bool = False):
        if all is True:
            Player.delete_all_players()
        elif player:
            player.delete_a_player()
