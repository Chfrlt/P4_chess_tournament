from models.player_model import Player
from views.player_views import PlayerView


class PlayerControl:

    def create_player() -> Player:
        player_parameters = PlayerView.creator_view()
        new_player = Player(
            player_parameters['first_name'],
            player_parameters['surname'],
            player_parameters['birthdate'],
            player_parameters['gender'],
            player_parameters['elo']
        )
        Player.insert(new_player)
        return new_player




    def selector(player_list = Player.get_players_in_db()):
        if len(player_list) == 0:
            PlayerView.selector_view()
        else:
            PlayerView.selector_view(player_list)
            selection = input()
            player_selection = player_list[int(selection) - 1]
            return player_selection

                
    def show_players_unsorted():
        PlayerView.print_players_unsorted(Player.get_players_in_db())


    def show_players_name_sorted():
        PlayerView.print_players_name_sorted(
            sorted(Player.get_players_in_db(), key=lambda x: x.surname))


    def show_players_elo_sorted():
        PlayerView.print_players_elo_sorted(
            sorted(Player.get_players_in_db(), key=lambda x: x.elo))


    def show_players_score_sorted():
        PlayerView.print_players_score_sorted(
                    sorted(Player.get_players_in_db(), key=lambda x: x.score))

    
    def update_elo():
        player = PlayerControl.selector()
        PlayerView.update_view('elo')
        new_elo = input()
        Player.update_elo(player, new_elo)