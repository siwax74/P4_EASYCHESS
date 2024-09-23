from easychess.utils.utils import Utils
from ..utils.player_validator import PlayerInputValidator
from ..utils.sanitize import Sanitize
from ..views.main_view import MainView
from ..views.player_view import PlayerView
from ..models.player import Player
from settings import PLAYERS_FILE


class PlayerManagerController:
    """
    Controller class for managing players.
    """

    def __init__(self):
        """
        Initializes the controller with a view, a filepath, and other necessary components.

        Attributes:
        - main_view (MainView): The main view for displaying menus.
        - view (PlayerView): The view for displaying player-related information.
        - filepath (str): The path to the players file.
        - sanitize (Sanitize): Utility for sanitizing input.
        - utils (Utils): General utility functions.
        - input_validator (PlayerInputValidator): Validator for player input.
        """
        self.main_view = MainView()
        self.view = PlayerView()
        self.filepath = PLAYERS_FILE
        self.sanitize = Sanitize(self.view)
        self.utils = Utils()
        self.input_validator = PlayerInputValidator(self.utils, self.sanitize)

    ############################################################################################################
    #                                           PLAYER MENU                                                    #
    ############################################################################################################
    def show_menu_options(self):
        """
        Displays the player menu and handles user choices.

        The method continuously prompts the user for a menu option and executes
        the corresponding action until the user decides to exit.
        """
        while True:
            choice = self.view.display_player_menu()
            valid_choice = self.input_validator.validate_choice(choice)
            if valid_choice == "1":
                self.create_player()
            elif valid_choice == "2":
                self.display_all_players()
            elif valid_choice == "3":
                self.main_view.display_menu()
            elif valid_choice == "0":
                break

    ############################################################################################################
    #                                       CHOICE 1       CREATE PLAYER                                      #
    ############################################################################################################
    def create_player(self):
        """
        Gathers player information and creates a new player.

        If player information is successfully gathered, a new player is created,
        saved to the file, and a success message is displayed.

        Returns:
        - Player: The newly created player object, or False if creation failed.
        """
        player_info = self.gather_player_information()
        if not player_info:
            return False
        new_player = Player.create(player_info)
        Player.save(self.filepath, new_player.as_dict())
        self.utils.display_success(f"Joueurs {new_player.first_name}, ajouté avec succès ! ")
        return new_player

    ############################################################################################################
    #                                           GATHER PLAYER INFO                                             #
    ############################################################################################################
    def gather_player_information(self):
        """
        Handles the flow for prompting and gathering information to create a new player.

        Prompts the user for the player's first name, last name, birthdate, and national ID.
        Returns a tuple containing the player's information or False if any input validation fails.

        Returns:
        - tuple: A tuple containing first name, last name, birthdate, and national ID,
                 or False if information gathering failed.
        """
        while True:
            first_name = self.input_validator.validate_info(self.view.ask_first_name)
            if first_name is False:
                break
            last_name = self.input_validator.validate_info(self.view.ask_last_name)
            if last_name is False:
                break
            birthdate = self.input_validator.validate_birthdate(self.view.ask_birthdate)
            if birthdate is False:
                break
            national_id = self.input_validator.validate_national_id(self.view.ask_national_id)
            if national_id is False:
                break
            player_info = first_name, last_name, birthdate, national_id
            return player_info

    ############################################################################################################
    #  CHOICE 2    SHOW BDD LIST PLAYERS                                                                      #
    ############################################################################################################
    def display_all_players(self):
        """
        Displays all players by reading from the specified file.

        The method retrieves player data, formats it for display, and shows it to the user.
        The user can return to the menu after viewing the list.

        Returns:
        - None
        """
        while True:
            players_data = Player.read(self.filepath)
            players = [Player.from_dict(player_data) for player_data in players_data]
            formatted_players = [f"{i+1}. {str(player)}" for i, player in enumerate(players)]
            self.view.display_player_list("\n".join(formatted_players))
            go_menu = self.input_validator.validate_return_to_menu(self.view.ask_return_menu)
            if go_menu:
                break
