from datetime import datetime
import re
from models.player import Player
from views.main_view import MainView
from views.player_view import PlayerView
from settings import PLAYERS_FILE


class PlayerManagerController:
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
        self.input_validator = PlayerInputValidator(self.view)

    ############################################################################################################
    #                                           PLAYER MENU                                                    #
    ############################################################################################################
    def show_menu_options(self):
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
        player_info = self.gather_player_information()
        if not player_info:
            return False
        new_player = Player.create(player_info)
        Player.save(self.filepath, new_player.as_dict())
        self.view.display_success(f"Joueurs {new_player.first_name}, ajouté avec succès ! ")
        return new_player.as_dict()
        ############################################################################################################
        #                                           GATHER PLAYER INFO                                             #
        ############################################################################################################

    def gather_player_information(self):
        """
        Handles the flow for prompting and creating a new player.
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
        Displays all players by reading from a file and passing formatted player information to the view.
        """
        while True:
            players_data = Player.read(self.filepath)
            players = [Player.from_dict(player_data) for player_data in players_data]
            formatted_players = [f"{i+1}. {str(player)}" for i, player in enumerate(players)]
            self.view.display_player_list("\n".join(formatted_players))
            go_menu = self.input_validator.validate_return_to_menu(self.view.ask_return_menu)
            if go_menu:
                break


############################################################################################################
#  VALIDATOR                                                                                               #
############################################################################################################
class PlayerInputValidator:
    def __init__(self, view):
        self.view = view

    ############################################################################################################
    #                                                VALID INPUT                                               #
    ############################################################################################################
    def validate_return_to_menu(self, input_function):
        while True:
            response = input_function().strip()
            if response == "0":
                return response
            else:
                self.view.display_error("Saisir 0 pour revenir au menu !")
                return False

    ############################################################################################################
    #                                                VALID CHOICE MENU                                         #
    ############################################################################################################
    def validate_choice(self, choice):
        """
        Prompt and validate the user's choice.
        """
        if choice in ["0", "1", "2", "3"]:
            return choice
        else:
            self.view.display_error("Veuillez saisir un choix entre 0, 1, 2 ou 3 !")
            return False

    ############################################################################################################
    #                                                INFO_NAME/SURNAME                                         #
    ############################################################################################################
    def validate_info(self, input_function):
        while True:
            info = input_function().strip()
            if re.match("^[A-Za-zÀ-ÖØ-öø-ÿ' -]+$", info):
                sanitize_info = self.sanitize_text(info)
                return sanitize_info
            elif info == "0":
                return False
            elif not re.match("^[A-Za-zÀ-ÖØ-öø-ÿ' -]+$", info):
                self.view.display_error("Le Prénom/Nom ne peut pas contenir de caractères spéciaux !")

    ############################################################################################################
    #                                                BIRTHDATE                                                 #
    ############################################################################################################
    def validate_birthdate(self, input_function):
        while True:
            birthdate = input_function()
            try:
                datetime.strptime(birthdate, "%d/%m/%Y")
                return birthdate
            except ValueError:
                if birthdate == "0":
                    return False
                else:
                    self.view.display_error("Veuillez saisir une date au format 'dd/mm/YYYY' !")

    ############################################################################################################
    #                                                NATIONAL_ID                                               #
    ############################################################################################################
    def validate_national_id(self, input_function):
        while True:
            national_id = input_function()
            if national_id == "0":
                return False
            if not national_id:
                return national_id
            elif len(national_id) > 7 or not re.match("^[A-Za-z0-9]{2}[0-9]{5}$", national_id):
                self.view.display_error("Veuillez saisir un national_id valide au format 'AB12345' !")
            else:
                return national_id

    ############################################################################################################
    #                                                SANITIZE_TEXT                                             #
    ############################################################################################################
    def sanitize_text(self, text):
        """
        Replace accented characters with their non-accented counterparts.
        """
        accents = {
            "é": "e",
            "è": "e",
            "à": "a",
            "ù": "u",
            "ç": "c",
            "â": "a",
            "ê": "e",
            "î": "i",
            "ô": "o",
            "û": "u",
            "ä": "a",
            "ë": "e",
            "ï": "i",
            "ö": "o",
            "ü": "u",
            "ÿ": "y",
        }
        for accented, non_accented in accents.items():
            text = text.replace(accented, non_accented)
        return text
