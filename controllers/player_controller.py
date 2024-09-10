from datetime import datetime
import re
import time
from models.player import Player
from views.main_view import MainView
from views.player_view import PlayerView
from settings import PLAYERS_FILE


class PlayerController:
    """
    Controller class for managing players.
    """

    def __init__(self):
        """
        Initializes the controller with a view and a filepath.
        """
        self.main_view = MainView()
        self.view = PlayerView()
        self.filepath = PLAYERS_FILE
        self.validator = PlayerValidator(self.view)

    def display_menu(self):
        """
        Displays the player menu, gets and handles the user's choice.
        """
        choice = self.view.display_player_menu()
        valid_choice = self.validator.prompt_valid_choice(choice)
        self.handle_user_choice(valid_choice)

    def handle_user_choice(self, choice):
        """
        Handles user choice after validation.
        """
        if choice == "1":
            self.prompt_player_information()
        elif choice == "2":
            self.display_all_players()
        elif choice == "3":
            self.main_view.display_menu()
        else:
            self.view.display_error(f"Veuillez choisir entre 1, 2 ou 3.")

    ############################################################################################################
    #  CHOICE 1       CREATE PLAYER                                                                            #
    ############################################################################################################
    def prompt_player_information(self):
        """
        Handles the flow for prompting and creating a new player.
        """
        first_name = self.validator.prompt_valid_first_name(self.view.ask_first_name)
        last_name = self.validator.prompt_valid_last_name(self.view.ask_last_name)
        birthdate = self.validator.prompt_valid_birthdate(self.view.ask_birthdate)
        national_id = self.validator.prompt_valid_national_id(self.view.ask_national_id)
        return self.create_player(first_name, last_name, birthdate, national_id)

    def create_player(self, first_name, last_name, birthdate, national_id):
        """
        Creates a player and saves their information.
        """
        player = Player.create(first_name, last_name, birthdate, national_id)
        return self.save_player(player.as_dict())

    def save_player(self, player_data):
        """
        Saves the player's information to the file.
        """
        Player.save(self.filepath, player_data)
        return self.view.display_success(
            f"Joueur : {player_data['last_name']}, ajouté à la base de données"
        )

    ############################################################################################################
    #  CHOICE 2    SHOW BDD LIST PLAYERS                                                                       #
    ############################################################################################################
    def display_all_players(self):
        """
        Placeholder for displaying all players.
        """
        players = Player.read(self.filepath)
        return self.view.display_player_list(players)
    

############################################################################################################
#  VALIDATOR                                                                                               #
############################################################################################################
class PlayerValidator:
    def __init__(self, view):
        self.view = view
    ############################################################################################################
    #                                                VALID CHOICE                                              #
    ############################################################################################################
    def prompt_valid_choice(self, choice):
        """
        Prompt and validate the user's choice.
        """
        while True:
            if self.is_valid_choice(choice):
                return choice
            else:
                self.view.display_error(
                    "Veuillez choisir une option valide : 1, 2 ou 3."
                )
                choice = self.view.display_player_menu()

    def is_valid_choice(self, choice):
        """
        Check if the choice is valid (i.e. one of '1', '2', or '3').
        """
        return choice in ["1", "2", "3"]

    ############################################################################################################
    #                                                FIRST_NAME                                                #
    ############################################################################################################
    def prompt_valid_first_name(self, input_function):
        while True:
            first_name = input_function().strip()
            if self.is_valid_first_name_format(first_name):
                return first_name

    def is_valid_first_name_format(self, first_name):
        if len(first_name) < 2 or len(first_name) > 20:
            self.view.display_error("Veuillez saisir un Nom valide !")
            return False
        if not re.match("^[A-Za-zÀ-ÖØ-öø-ÿ' -]+$", first_name):
            self.view.display_error(
                "Le nom ne peut pas contenir de caractères spéciaux !"
            )
            return False
        return True

    ############################################################################################################
    #                                                LAST_NAME                                                 #
    ############################################################################################################
    def prompt_valid_last_name(self, input_function):
        while True:
            last_name = input_function().strip()
            if self.is_valid_last_name_format(last_name):
                return last_name

    def is_valid_last_name_format(self, last_name):
        if len(last_name) < 2 or len(last_name) > 30:
            self.view.display_error("Veuillez saisir un Prénom valide !")
            return False
        if not re.match("^[A-Za-zÀ-ÖØ-öø-ÿ' -]+$", last_name):
            self.view.display_error(
                "Le prénom ne peut pas contenir de caractères spéciaux !"
            )
            return False
        return True

    ############################################################################################################
    #                                                BIRTHDATE                                                 #
    ############################################################################################################
    def prompt_valid_birthdate(self, input_function):
        while True:
            birthdate = input_function()
            if self.is_valid_birthdate_format(birthdate):
                return birthdate

    def is_valid_birthdate_format(self, birthdate):
        try:
            datetime.strptime(birthdate, "%d/%m/%Y")
            return True
        except ValueError:  # Attrape l'exception si la conversion échoue
            self.view.display_error("Veuillez saisir une date au format 'dd/mm/YYYY' !")
            return False  # Si la conversion échoue, la date est invalide

    ############################################################################################################
    #                                                NATIONAL_ID                                               #
    ############################################################################################################
    def prompt_valid_national_id(self, input_function):
        while True:
            national_id = input_function()
            if self.is_valid_national_id_format(national_id):
                return national_id

    def is_valid_national_id_format(self, national_id):
        if not national_id:
            return True
        if len(national_id) > 7 or not re.match(
            "^[A-Za-z0-9]{2}[0-9]{5}$", national_id
        ):
            self.view.display_error(
                "Veuillez saisir un national_id valide au format 'AB12345' !"
            )
            return False
        return True
