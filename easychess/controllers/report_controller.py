from easychess.models.player import Player
from easychess.models.tournament import Tournament
from easychess.utils.reports_validator import ReportsInputValidator
from easychess.utils.utils import Utils
from easychess.views.report_view import ReportView
from settings import PLAYERS_FILE, TOURNAMENTS_FILE


class ReportManagerController:
    def __init__(self):
        """
        Initializes the ReportManagerController with necessary components.

        Attributes:
        - view (ReportView): The view component for displaying reports.
        - db_players (str): The path to the players file.
        - db_tournaments (str): The path to the tournaments file.
        - utils (Utils): Utility functions for the controller.
        - input_validator (ReportsInputValidator): Validator for report inputs.
        """
        self.view = ReportView()
        self.db_players = PLAYERS_FILE
        self.db_tournaments = TOURNAMENTS_FILE
        self.utils = Utils()
        self.input_validator = ReportsInputValidator(self.utils)

    def show_menu_options(self):
        """
        Displays the report menu and handles user choices.

        The method continuously prompts the user for a menu option and executes
        the corresponding action until the user decides to exit.
        """
        while True:
            menu_choice = self.view.display_reports_menu()
            valid_choice = self.input_validator.validate_menu_choice(menu_choice)
            if valid_choice == "1":
                self.get_alphabetical_players()
            elif valid_choice == "2":
                self.get_all_tournaments()
            elif valid_choice == "3":
                self.get_tournament_by_name()
            elif valid_choice == "0":
                break

    def get_alphabetical_players(self):
        """
        Retrieves and displays the list of players sorted in alphabetical order.

        The method reads player data from the specified file, sorts the players
        by last name, and formats the output for display.
        """
        players = Player.read(self.db_players)
        players.sort(key=lambda x: x["last_name"])
        formatted_players = [
            f"{player['last_name']} {player['first_name']} - "
            f"{player['birthdate']} - National ID: {player['national_id']}"
            for player in players
        ]
        self.view.display_alphabetical_players(formatted_players)

    def get_all_tournaments(self):
        """
        Retrieves and displays all tournaments from the specified file.

        The method reads tournament data and formats it for display.
        """
        tournaments = Tournament.read(self.db_tournaments)
        self.view.display_all_tournaments(tournaments)

    def get_tournament_by_name(self):
        """
        Retrieves and displays details of a tournament by its name.

        The method prompts the user for a tournament name, validates the input,
        and if found, displays the tournament details along with the players
        ranked by their scores.
        """
        tournaments = Tournament.read(self.db_tournaments)
        self.view.display_tournaments_name(tournaments)
        tournament_name = self.input_validator.validate_tournament_name(
            self.view.ask_tournament_name_input, tournaments
        )
        if tournament_name:
            for tournament in tournaments.values():
                players = tournament["players"]
                players.sort(key=lambda x: x["last_name"])
                ranking_players = sorted(players, key=lambda x: x["score"], reverse=True)
                self.view.display_tournament_details(tournament, ranking_players)
                break
