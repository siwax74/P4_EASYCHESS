from datetime import datetime
import re
from models.player import Player
from models.tournament import Tournament
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
        self.validator = TournamentValidator(self.view, self.file_player)

    def display_menu(self):
        """
        Displays the tournament menu and gets the user's choice.
        """
        choice = self.view.display_tournament_menu()
        valid_choice = self.validator.prompt_valid_choice(choice)
        self.handle_user_choice(valid_choice)

    def handle_user_choice(self, choice):
        """
        Handles user choice after validation.
        """
        if choice == "1":
            self.prompt_tournament_information()
        elif choice == "2":
            self.display_tournament_list()
        elif choice == "3":
            self.display_tournaments()
        elif choice == "0":
            print("Retour au menu principal...")
        else:
            self.view.display_error("Choix invalide")
            self.display_menu()

    def prompt_tournament_information(self):
        """
        Handles the flow for prompting and creating a new tournament.
        """
        name = self.validator.prompt_valid_name(self.view.ask_name)
        location = self.validator.prompt_valid_location(self.view.ask_location)
        start_date = self.validator.prompt_valid_start_date(self.view.ask_start_date)
        end_date = self.validator.prompt_valid_end_date(self.view.ask_end_date)
        description = self.validator.prompt_valid_description(self.view.ask_description)
        return self.create_tournament(name, location, start_date, end_date, description)
    
    def create_tournament(self, name, location, start_date, end_date, description):
        """
        Creates a tournament and saves its information.
        """
        tournament = Tournament.create(
            name=name,
            location=location,
            start_date=start_date,
            end_date=end_date,
            description=description,
        )
        return self.select_players(tournament.as_dict())

    def select_players(self, tournament_data):
        choice = self.view.ask_player_registration_method()
        valid_method = self.validator.validate_player_registration_method(choice)
        return self.handle_player_registration_method(valid_method, tournament_data)

    def handle_player_registration_method(self, valid_method, tournament_data):
        if valid_method == "1":
            return self.add_player_auto(tournament_data)
        elif valid_method == "2":
            return self.prompt_selected_player(tournament_data)

    def add_player_auto(self, tournament_data):
        """
        Calls the model method to add players from the file.
        """
        try:
            tournament_player = Tournament.add_player_auto(self.file_player, tournament_data)
            return self.save_tournament(tournament_player)
        except Exception as e:
            self.view.display_error(f"Une erreur est survenue : {str(e)}")

    def prompt_selected_player(self, tournament_data):
        players = Player.read(self.file_player)
        print(players)
        selected_players = self.view.ask_player_selection(players)
        return self.add_player_manual(selected_players, players, tournament_data)
       
    def add_player_manual(self, player_index, players, tournament_data):
        tournament_player = Tournament.add_player_manual(player_index, players, tournament_data)
        return self.save_tournament(tournament_player)

    def save_tournament(self, tournament_data):
        """
        Saves the tournament's information to the file.
        """
        Tournament.save(self.file_tournament, tournament_data)
        tournament_name = tournament_data.get("name")
        return self.view.display_success(f"Tous les joueurs ont été ajouté au tournois, {tournament_name} ! ")   

############################################################################################################
#  VALIDATOR                                                                                               #
############################################################################################################
class TournamentValidator:
    def __init__(self, view, file_player):
        self.view = view
        self.file_player = file_player
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
                    "Veuillez choisir une option valide : 1, 2, 3 ou 0."
                )
                choice = self.view.display_tournament_menu()

    def is_valid_choice(self, choice):
        """
        Check if the choice is valid (i.e. one of '1', '2', '3' or '0').
        """
        return choice in ["1", "2", "3", "0"]

    ############################################################################################################
    #                                                VALID NAME                                                #
    ############################################################################################################
    def prompt_valid_name(self, input_function):
        while True:
            name = input_function().strip()
            if self.is_valid_name_format(name):
                return name

    def is_valid_name_format(self, name):
        if len(name) < 2 or len(name) > 50:
            self.view.display_error("Veuillez saisir un nom valide !")
            return False
        if not re.match("^[A-Za-zÀ-ÖØ-öø-ÿ' -]+$", name):
            self.view.display_error(
                "Le nom ne peut pas contenir de caractères spéciaux !"
            )
            return False
        return True

    ############################################################################################################
    #                                                LOCATION                                                  #
    ############################################################################################################
    def prompt_valid_location(self, input_function):
        while True:
            location = input_function().strip()
            if self.is_valid_location_format(location):
                return location

    def is_valid_location_format(self, location):
        if len(location) < 2 or len(location) > 50:
            self.view.display_error("Veuillez saisir un lieu valide !")
            return False
        if not re.match("^[A-Za-zÀ-ÖØ-öø-ÿ' -]+$", location):
            self.view.display_error(
                "Le lieu ne peut pas contenir de caractères spéciaux !"
            )
            return False
        return True

    ############################################################################################################
    #                                                DESCRIPTION                                              #
    ############################################################################################################
    def prompt_valid_description(self, input_function):
        while True:
            description = input_function().strip()
            if self.is_valid_description_format(description):
                return description

    def is_valid_description_format(self, description):
        if len(description) < 2 or len(description) > 200:
            self.view.display_error("La description doit être entre 5 et 200 caractères !")
            return False
        return True

    ############################################################################################################
    #                                                START DATE                                               #
    ############################################################################################################
    def prompt_valid_start_date(self, input_function):
        while True:
            start_date = input_function().strip()
            if self.is_valid_start_date_format(start_date):
                return start_date
    def is_valid_start_date_format(self, date_str):
        try:
            datetime.strptime(date_str, "%d/%m/%Y %H:%M")
            return True
        except ValueError:
            self.view.display_error("Veuillez saisir une date au format 'dd/mm/YYYY' !")
            return False        

    ############################################################################################################
    #                                                END DATE                                                 #
    ############################################################################################################
    def prompt_valid_end_date(self, input_function):
        while True:
            end_date = input_function().strip()
            if end_date == "" or self.is_valid_end_date_format(end_date):
                return end_date

    def is_valid_end_date_format(self, date_str):
        try:
            datetime.strptime(date_str, "%d/%m/%Y")
            return True
        except ValueError:
            self.view.display_error("Veuillez saisir une date au format 'dd/mm/YYYY' !")
            return False

    ############################################################################################################
    #                                                PLAYERS                                                   #
    ############################################################################################################
    def validate_player_registration_method(self, choice):
        while True:
            if self.is_valid_player_registration_methode(choice):
                return choice
            else:
                self.view.display_error(
                    "Veuillez choisir une option valide : 1, 2 ou 0."
                )
                choice = self.view.display_tournament_menu()

    def is_valid_player_registration_methode(self, choice):
        """
        Check if the choice is valid (i.e. one of '1', '2' or '0').
        """
        return choice in ["1", "2", "0"]