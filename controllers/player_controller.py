from datetime import datetime
import re
from models.player import Player
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
        self.view = PlayerView()
        self.filepath = PLAYERS_FILE
        self.validator = PlayerValidator(self.view)

    def display_menu(self):
        """
        Displays the player menu and gets the user's choice.
        """
        choice = self.view.display_player_menu()
        self.handle_user_choice(choice)

    def handle_user_choice(self, choice):
        if choice == "1":
            self.prompt_player_information()
        elif choice == "2":
            self.display_all_players()
        elif choice == "3":
            pass

    def prompt_player_information(self):
        first_name = self.validator.prompt_valid_first_name(self.view.ask_first_name)
        last_name = self.validator.prompt_valid_last_name(self.view.ask_last_name)
        birthdate = self.validator.prompt_valid_birthdate(self.view.ask_birthdate)
        national_id = self.validator.prompt_valid_national_id(self.view.ask_national_id)
        return self.add_player_to_database(first_name, last_name, birthdate, national_id)

    def add_player_to_database(self, first_name, last_name, birthdate, national_id):
        player = Player.create(first_name, last_name, birthdate, national_id)
        player_data = player.as_dict()
        player.save(self.filepath)
        return self.view.display_success(f"Joueur : {player_data}, ajouté a la base de donnée")


############################################################################################################
#  VALIDATOR                                                                                               #
############################################################################################################   
class PlayerValidator:
    def __init__(self, view):
        self.view = view
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
            self.view.display_error("Veuillez saisir un Nom !")
            return False
        if not re.match("^[A-Za-zÀ-ÖØ-öø-ÿ' -]+$", first_name):
            self.view.display_error("Le nom ne peut pas contenir de carractères spéciaux !")
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
            self.view.display_error("Veuillez saisir un Prénom !")
            return False
        if not re.match("^[A-Za-zÀ-ÖØ-öø-ÿ' -]+$", last_name):
            self.view.display_error("Le Prénom ne peut pas contenir de carractères spéciaux !")
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
            self.view.display_error("Veuillez saisir une date format 'dd/mm/YYYY' !")
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
        if len(national_id) > 7:
            self.view.display_error("Veuillez saisir national_id format 'AB12345' !")
            return False
        return True
        
            

