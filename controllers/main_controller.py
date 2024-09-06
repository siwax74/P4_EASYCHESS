import sys
import time
from controllers.player_controller import PlayerController
from controllers.tournament_controller import TournamentController
from views.main_view import MainView


def run() -> None:
    while True:
        main_menu_choice = MainView.display_menu()

        if main_menu_choice == "1":
            player_controller = PlayerController()
            player_controller.display_menu()

        elif main_menu_choice == "2":
            tournament_controller = TournamentController()
            tournament_controller.display_menu()

        elif main_menu_choice == "4":
            pass

        elif main_menu_choice == "5":
            print("Vous quittez le programme. Merci pour votre soutien !")
            time.sleep(2)
            sys.exit(0)

        else:
            print("Veuillez saisir un nombre parmi 1, 2, 3, 4 ou 5.")
            time.sleep(2)
