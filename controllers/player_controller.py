from datetime import datetime
from models.player import Player
from views.player_view import PlayerView
from settings import PLAYERS_FILE
from utils.utils import load_from_json, set_player_to_json


class PlayerController:
    """
    Controller class for managing players.
    """

    def __init__(self):
        """
        Initializes the controller with a view and a filepath.
        """
        self.view = PlayerView()
        self.filepath = PLAYERS_FILE

    def display_menu(self):
        """
        Displays the player menu and gets the user's choice.
        """
        choice = self.view.display_player_menu()
        self.get_choice(choice)

    def get_choice(self, choice):
        """
        Processes the user's choice.

        Args:
            choice (str): The user's choice (1 or 2)
        """
        if choice == "1":
            self.create_player()
        elif choice == "2":
            self.display_player_list()
        else:
            self.view.display_error("Choix invalide")

    def get_player_info(self):
        """
        Gets the player's information from the user.

        Returns:
            tuple: (first_name, last_name, birthdate, national_id)
        """
        first_name = self._get_valid_input(
            self.view.ask_first_name, "Le prénom est obligatoire"
        )
        last_name = self._get_valid_input(
            self.view.ask_last_name, "Le nom est obligatoire"
        )
        birthdate = self._get_valid_date(self.view.ask_birthdate)
        national_id = self.view.ask_national_id()
        return first_name, last_name, birthdate, national_id

    def _create_player(self, first_name, last_name, birthdate, national_id):
        """
        Creates a new player object.

        Args:
            first_name (str): The player's first name
            last_name (str): The player's last name
            birthdate (str): The player's birthdate (DD/MM/YYYY)
            national_id (str): The player's national ID

        Returns:
            dict: The player's information as a dictionary
        """
        player = Player(first_name, last_name, birthdate, national_id)
        return player.as_dict()

    def save_player_to_json(self, player):
        """
        Saves the player's information to a JSON file.

        Args:
            player (dict): The player's information as a dictionary
        """
        set_player_to_json(player, self.filepath)

    def create_player(self):
        """
        Creates a new player and saves it to the JSON file.
        """
        first_name, last_name, birthdate, national_id = self.get_player_info()
        player = self._create_player(first_name, last_name, birthdate, national_id)
        self.save_player_to_json(player)
        self.view.display_success("Le joueur a été créé avec succès!")

    def display_player_list(self):
        """
        Displays the list of players from the JSON file.
        """
        while True:
            players = load_from_json(self.filepath)
            self.view.player_list(players)
            if self.view.ask_to_return_to_menu():
                break

    def _get_valid_input(self, input_function, error_message):
        """
        Gets a valid input from the user.

        Args:
            input_function (callable): The function to get the input from
            error_message (str): The error message to display if the input is invalid

        Returns:
            str: The valid input
        """
        value = None
        while value is None:
            value = input_function()
            if not value:
                self.view.display_error(error_message)
                value = None
        return value

    def _get_valid_date(self, input_function):
        """
        Gets a valid date from the user.

        Args:
            input_function (callable): The function to get the input from

        Returns:
            str: The valid date (DD/MM/YYYY)
        """
        date_str = None
        while date_str is None:
            date_str = input_function()
            try:
                datetime.strptime(date_str, "%d/%m/%Y")
            except ValueError:
                self.view.display_error(
                    "La date de naissance est invalide, format : DD/MM/YYYY"
                )
                date_str = None
        return date_str
