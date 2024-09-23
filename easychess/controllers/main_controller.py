import sys
import time
from easychess.controllers.report_controller import ReportManagerController
from ..views.main_view import MainView
from .player_controller import PlayerManagerController
from .tournament_controller import TournamentManagerController


def run() -> None:
    """
    Runs the main loop of the application, presenting a menu to the user
    and delegating control to the respective controllers based on the user's choice.

    The function displays a menu with several options and waits for the user to select
    an option. Depending on the user's choice, the program will either:
    - Launch the PlayerManagerController (option "1")
    - Launch the TournamentManagerController (option "2")
    - Launch the ReportManagerController (option "3")
    - Exit the program (option "4")

    This function runs indefinitely until the user chooses to exit by selecting option "4".
    """
    while True:
        main_menu_choice = MainView.display_menu()  # Display main menu and get user input

        if main_menu_choice == "1":
            # Initialize and show menu options for Player Management
            player_controller = PlayerManagerController()
            player_controller.show_menu_options()

        elif main_menu_choice == "2":
            # Initialize and show menu options for Tournament Management
            tournament_controller = TournamentManagerController()
            tournament_controller.show_menu_options()

        elif main_menu_choice == "3":
            # Initialize and show menu options for Report Management
            raport_controller = ReportManagerController()
            raport_controller.show_menu_options()

        elif main_menu_choice == "4":
            # Exit the application gracefully
            print("Vous quittez le programme. Merci pour votre soutien !")
            time.sleep(2)
            sys.exit(0)
