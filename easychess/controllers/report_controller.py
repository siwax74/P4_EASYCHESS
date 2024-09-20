from easychess.models.player import Player
from easychess.utils.reports_validator import ReportsInputValidator
from easychess.views.report_view import ReportView
from settings import PLAYERS_FILE, TOURNAMENTS_FILE


class ReportManagerController:
    def __init__(self):
        self.view = ReportView()
        self.db_players = PLAYERS_FILE
        self.db_tournaments = TOURNAMENTS_FILE
        self.input_validator = ReportsInputValidator(self.view)

    def show_menu_options(self):
        while True:
            menu_choice = self.view.display_reports_menu()
            valid_choice = self.input_validator.validate_menu_choice(menu_choice)
            if valid_choice == "1":
                self.get_alphabetical_players()
            elif valid_choice == "2":
                self.get_all_tournaments()
            elif valid_choice == "0":
                break

    def get_alphabetical_players(self):
        players = Player.read(self.db_players)
        players.sort(key=lambda x: x["last_name"])
        formatted_players = [
            f"{player['last_name']} {player['first_name']} - {player['birthdate']} - National ID: {player['national_id']}"
            for player in players
        ]
        self.view.display_alphabetical_players(formatted_players)
