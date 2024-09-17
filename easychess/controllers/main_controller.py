import sys
import time
from ..views.main_view import MainView
from .player_controller import PlayerManagerController
from .tournament_controller import TournamentManagerController


def run() -> None:
    while True:
        main_menu_choice = MainView.display_menu()
        if main_menu_choice == "1":
            player_controller = PlayerManagerController()
            player_controller.show_menu_options()

        elif main_menu_choice == "2":
            tournament_controller = TournamentManagerController()
            tournament_controller.show_menu_options()

        elif main_menu_choice == "3":
            print("Vous quittez le programme. Merci pour votre soutien !")
            time.sleep(2)
            sys.exit(0)

        else:
            print("Veuillez saisir un nombre parmi 1, 2, ou 3.")
            time.sleep(2)
