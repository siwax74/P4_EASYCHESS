from easychess.utils.utils import Utils
from ..utils.player_validator import PlayerInputValidator
from ..utils.sanitize import Sanitize
from ..views.main_view import MainView
from ..views.player_view import PlayerView
from ..models.player import Player
from settings import PLAYERS_FILE


class PlayerManagerController:
    """
    Controller class for managing player-related operations such as creating a player
    and displaying all players.
    """

    def __init__(self):
        """
        Initializes the PlayerManagerController with the required views, utilities, and validation tools.

        Attributes:
            main_view (MainView): The main view object for general application display.
            view (PlayerView): The view object for displaying player-related interfaces.
            filepath (str): The path to the file where player data is stored.
            sanitize (Sanitize): A sanitization object to clean user inputs.
            utils (Utils): Utility functions for general use.
            input_validator (PlayerInputValidator): A validator for ensuring player input correctness.
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
        Displays the player management menu and handles user input.
        The user can choose to create a player, display all players, or return to the main menu.
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

            ###########################################################################################################
            #                                       CHOICE 1       CREATE PLAYER                                      #
            ###########################################################################################################

    def create_player(self):
        """
        Handles the process of gathering player information and creating a new player.
        The new player is saved to the file specified in `self.filepath`.

        Returns:
            Player: The newly created player object, or False if player creation was unsuccessful.
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
        Prompts the user for all necessary player information (first name, last name, birthdate, national ID)
        and validates each input.

        If validation fails at any point, the player creation process is aborted.

        Returns:
            tuple: A tuple containing player information (first_name, last_name, birthdate, national_id),
            or None if the process is interrupted.
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

            ###########################################################################################################
            #  CHOICE 2    SHOW BDD LIST PLAYERS                                                                      #
            ###########################################################################################################

    def display_all_players(self):
        """
        Reads player data from the file and displays a list of all players.
        The user can return to the player menu after viewing the list.
        """
        while True:
            players_data = Player.read(self.filepath)
            players = [Player.from_dict(player_data) for player_data in players_data]
            formatted_players = [f"{i+1}. {str(player)}" for i, player in enumerate(players)]
            self.view.display_player_list("\n".join(formatted_players))
            go_menu = self.input_validator.validate_return_to_menu(self.view.ask_return_menu)
            if go_menu:
                break
