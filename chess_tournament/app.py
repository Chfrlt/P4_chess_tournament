from controllers.menus_controller import MenuControl
from controllers.player_controller import PlayerControl
from controllers.round_controller import RoundControl
from controllers.tournament_controller import TournamentControl


if __name__ == "__main__":
    a = PlayerControl()
    b = TournamentControl()
    c = RoundControl()
    user = MenuControl(a, b, c)

    user.main_menu()
    user.execute_menu()
