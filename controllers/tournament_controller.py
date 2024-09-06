from datetime import datetime
from models.tournament import Tournament
from utils import utils
from utils.utils import load_from_json, set_tournament_to_json
from views.main_view import MainView
from views.tournament_view import TournamentView
from settings import TOURNAMENT_FILE, PLAYERS_FILE


class TournamentController:
    """
    Controller class for managing tournaments.
    """

    def __init__(self):
        """
        Initializes the controller with a view and file paths.
        """
        self.view = TournamentView()
        self.file_tournament = TOURNAMENT_FILE
        self.file_player = PLAYERS_FILE

    def display_menu(self):
        """
        Displays the tournament menu and gets the user's choice.
        """
        choice = self.view.display_tournament_menu()
        self._process_choice(choice)

    def _process_choice(self, choice):
        """
        Processes the user's choice.

        Args:
            choice (str): The user's choice (1 or 2)
        """
        if choice == "1":
            self.create_tournament()
        elif choice == "2":
            self.display_tournament_list()
        elif choice == "0":
            print("Retour au menu principal...")
            self.display_menu()
        else:
            self.view.display_error("Choix invalide")
            self.display_menu()

    def create_tournament(self):
        """
        Creates a new tournament and saves it to the JSON file.
        """
        tournament_info = self._get_tournament_info()
        if tournament_info is None:
            return

        name, location, start_date, end_date, rounds, players = tournament_info
        self._create_tournament(name, location, start_date, end_date, rounds, players)
        self.view.display_success("Le tournoi a été créé avec succès!")
        self.display_menu()

    def _get_tournament_info(self):
        """
        Gets the tournament's information from the user.

        Returns:
            tuple: (name, location, start_date, end_date, rounds, players) or None if cancelled
        """
        name = self._get_valid_input(self.view.ask_name, "Le nom est obligatoire")
        if not name:
            self.view.display_error("Création de tournoi annulée.")
            return None

        location = self._get_valid_input(
            self.view.ask_location, "Le lieu est obligatoire"
        )
        if not location:
            self.view.display_error("Création de tournoi annulée.")
            return None

        start_date = self._get_valid_date(self.view.ask_start_date)
        if not start_date:
            self.view.display_error("Création de tournoi annulée.")
            return None

        end_date = self._get_valid_date(self.view.ask_end_date)
        if not end_date:
            self.view.display_error("Création de tournoi annulée.")
            return None

        rounds = self.view.ask_rounds()
        if not rounds:
            rounds = 4

        players = self._select_players()
        if not players:
            self.view.display_error("Création de tournoi annulée.")
            return None

        return name, location, start_date, end_date, rounds, players

    def _get_valid_input(self, input_function, error_message):
        """
        Gets a valid input from the user.

        Args:
            input_function (callable): The function to get the input from
            error_message (str): The error message to display if the input is invalid

        Returns:
            str: The valid input
        """
        while True:
            value = input_function()
            if value == "0":
                return None
            if value:
                return value
            self.view.display_error(error_message)

    def _get_valid_date(self, input_function):
        """
        Gets a valid date from the user.

        Args:
            input_function (callable): The function to get the input from

        Returns:
            str: The valid date (DD/MM/YYYY) or None if cancelled
        """
        while True:
            date_str = input_function()
            if date_str == "0":
                return None
            if self._is_valid_date(date_str):
                return date_str
            self.view.display_error("La date est invalide, format : DD/MM/YYYY")

    def _is_valid_date(self, date_str):
        """
        Checks if the provided date string is valid.

        Args:
            date_str (str): The date string to check

        Returns:
            bool: True if valid, False otherwise
        """
        for fmt in ["%d/%m/%Y", "%d/%m/%Y %H:%M"]:
            try:
                datetime.strptime(date_str, fmt)
                return True
            except ValueError:
                pass
        return False

    def _select_players(self):
        """
        Handles the process of selecting players for the tournament.

        Returns:
            list: List of selected players or None if cancelled
        """
        registration_method = self.view.ask_player_registration()
        if registration_method == "auto":
            pass
        else:
            players = load_from_json(self.file_player)
            if not players:
                print("Aucun joueur disponible.")
                return []

            self._display_players(players)
            selections = self.view.ask_player_selection()
            if selections is None:
                self.view.display_error("Sélection des joueurs annulée.")
                self.display_menu()
                return None

            return self._process_player_selections(selections, players)

    def _display_players(self, players):
        """
        Displays the list of available players.

        Args:
            players (dict): Dictionary of players
        """
        print("Liste des joueurs disponibles :")
        for i, (key, player) in enumerate(players.items(), start=1):
            print(f"{i}. {player['first_name']} {player['last_name']} (ID: {key})")

    def _process_player_selections(self, selections, players):
        """
        Processes the player's selections.

        Args:
            selections (str): Comma-separated string of player indices
            players (dict): Dictionary of available players

        Returns:
            list: List of selected players or None if cancelled
        """
        try:
            selected_indices = [int(x.strip()) for x in selections.split(",")]
        except ValueError:
            print(
                "Entrée non valide. Veuillez entrer des numéros séparés par des virgules."
            )
            return []

        selected_players = []
        for index in selected_indices:
            if 1 <= index <= len(players):
                key = list(players.keys())[index - 1]
                selected_players.append(players[key])
            else:
                print(f"Le numéro {index} est invalide.")

        while True:
            self.view.display_selected_players(selected_players)
            validation = input(
                "Appuyer sur Entrée pour valider les joueurs sélectionnés... "
            )
            if validation == "":
                break
            else:
                print(
                    "Veuillez appuyer sur Entrée pour valider les joueurs sélectionnés."
                )

        return selected_players

    def _create_tournament(
        self, name, location, start_date, end_date, number_of_rounds, players
    ):
        """
        Creates a new tournament object and saves it.

        Args:
            name (str): The tournament's name
            location (str): The tournament's location
            start_date (str): The tournament's start date (DD/MM/YYYY)
            end_date (str): The tournament's end date (DD/MM/YYYY)
            rounds (int): The number of rounds in the tournament
            players (list): List of players participating in the tournament
        """
        tournament = Tournament(
            name, location, start_date, end_date, number_of_rounds, players
        )

        return self._save_tournament(tournament)

    def _save_tournament(self, tournament):
        """
        Saves the tournament to the database.
        """

        return set_tournament_to_json(tournament.as_dict(), self.file_tournament)

    def display_tournament_list(self):
        """
        Displays a list of tournaments. (To be implemented as needed)
        """
        pass
