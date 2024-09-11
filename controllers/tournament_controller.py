from datetime import datetime
import re
import time
from controllers.player_controller import PlayerManagerController
from models.player import Player
from models.tournament import Tournament
from views.tournament_view import TournamentView
from settings import TOURNAMENT_FILE, PLAYERS_FILE


class TournamentManagerController:
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
        self.validator = TournamentInputValidator(self.view, self.file_player)

    def show_menu_options(self):
        """
        Displays the tournament menu and gets the user's choice.
        """
        menu_choice = self.view.display_tournament_menu()
        valid_choice = self.validator.validate_user_menu_choice(menu_choice)
        self.process_user_choice(valid_choice)

    ############################################################################################################
    #                                                GET CHOICE MENU OPTION                                    #
    ############################################################################################################
    def process_user_choice(self, menu_choice):
        """
        Processes user choice after validation.
        """
        if menu_choice == "1":
            self.gather_tournament_information()
        elif menu_choice == "2":
            self.display_all_tournaments()
        elif menu_choice == "3":
            self.display_tournaments()
        elif menu_choice == "0":
            print("Retour au menu principal...")
        else:
            self.view.display_error("Choix invalide")
            self.show_menu_options()

    ############################################################################################################
    #                                                IF CHOICE 1                                               #
    ############################################################################################################
    def gather_tournament_information(self):
        """
        Gathers information for creating a new tournament.
        """
        name = self.validator.validate_tournament_name(self.view.ask_name)
        location = self.validator.validate_tournament_location(self.view.ask_location)
        start_date = self.validator.validate_tournament_start_date(
            self.view.ask_start_date
        )
        end_date = self.validator.validate_tournament_end_date(self.view.ask_end_date)
        description = self.validator.validate_tournament_description(
            self.view.ask_description
        )
        return self.initialize_tournament(
            name, location, start_date, end_date, description
        )

    def initialize_tournament(self, name, location, start_date, end_date, description):
        """
        Initializes a tournament.
        """
        tournament = Tournament.create(
            name, location, start_date, end_date, description
        )
        return self.choose_player_registration_method(tournament.as_dict())

    def choose_player_registration_method(self, tournament_info):
        choice = self.view.ask_player_registration_method()
        valid_method = self.validator.validate_registration_method_choice(choice)
        return self.execute_registration_method(valid_method, tournament_info)

    def execute_registration_method(self, valid_method, tournament_info):
        if valid_method == "1":
            return self.register_players_automatically(tournament_info)
        elif valid_method == "2":
            return self.gather_manual_player_selection(tournament_info)
        elif valid_method == "3":
            self.player_manager_controller = PlayerManagerController()
            new_player = self.player_manager_controller.gather_player_information()
            return self.add_player_to_tournament(new_player, tournament_info)
        
    def add_player_to_tournament(self, new_player, tournament_info):
        print(new_player)
        print(tournament_info)
        tournament_info["players"].append(new_player)  # Add the new player to the tournament info
        self.update_tournament_file(tournament_info)  # Update the JSON file with the new tournament info
        print(tournament_info)
        return tournament_info

    def register_players_automatically(self, tournament_info):
        """
        Registers players automatically from the file.
        """
        try:
            tournament_player = Tournament.add_player_auto(
                self.file_player, tournament_info
            )
            return self.store_tournament_to_file(tournament_player)
        except Exception as e:
            self.view.display_error(f"Une erreur est survenue : {str(e)}")

    def gather_manual_player_selection(self, tournament_info):
        players = Player.read(self.file_player)
        player_indices = self.validator.validate_selected_players_input(
            self.view.ask_player_selection, players
        )
        return self.register_selected_players_manually(
            player_indices, players, tournament_info
        )

    def register_selected_players_manually(
        self, player_indices, players, tournament_info
    ):
        tournament_player = Tournament.add_player_manual(
            player_indices, players, tournament_info
        )
        return self.store_tournament_to_file(tournament_player)

    def store_tournament_to_file(self, tournament_info):
        """
        Persists the tournament's information to the file.
        """
        Tournament.save(self.file_tournament, tournament_info)
        return self.view.display_success(
            f"Tous les joueurs ont été ajoutés au tournoi, {tournament_info.get("name")} !"
        )

    ############################################################################################################
    #                                               IF CHOICE 2                                                #
    ############################################################################################################
    def display_all_tournaments(self):
        """
        Prépare les données pour afficher la liste des tournois à venir.
        """
        existing_tournaments = Tournament.read(self.file_tournament)
        
        if not existing_tournaments:
            self.view.display_error("Aucun tournois enregistré !")
            return
        upcoming_tournaments = {
            tournament_id: details
            for tournament_id, details in existing_tournaments.items()
            if details and details.get("a_venir", True)
        } 
        if not upcoming_tournaments:
            self.view.display_error("Aucun tournois a venir !")
            return
        
        tournament_data = []
        
        for tournament_id, details in upcoming_tournaments.items():
            tournament_info = {
                'id': tournament_id,
                'name': details.get("name", "Nom non disponible"),
                'location': details.get("location", "Emplacement non disponible"),
                'start_date': details.get("start_date", "Date de début non disponible"),
                'end_date': details.get("end_date", "Date de fin non disponible"),
                'number_of_rounds': details.get("number_of_rounds", "Nombre de tours non disponible"),
                'players': details.get("players", []),
                'current_round': details.get("current_round", "Tour actuel non disponible"),
                'list_rounds': details.get("list_rounds", []),
                'description': details.get("description", "Description non disponible")
            }
            player_details = []
            for player in tournament_info['players']:
                player_info = {
                    'last_name': player.get("last_name", "Nom de famille non disponible"),
                    'first_name': player.get("first_name", "Prénom non disponible"),
                    'birthdate': player.get("birthdate", "Date de naissance non disponible"),
                    'national_id': player.get("national_id", "Identifiant national non disponible")
                }
                player_details.append(player_info)
            
            tournament_info['player_details'] = player_details
            tournament_data.append(tournament_info)
    
        self.view.display_tournament_list(tournament_data)


############################################################################################################
#  VALIDATOR                                                                                               #
############################################################################################################
class TournamentInputValidator:
    def __init__(self, view, file_player):
        self.view = view
        self.file_player = file_player

    ############################################################################################################
    #                                                VALID MENU CHOICE                                         #
    ############################################################################################################
    def validate_user_menu_choice(self, menu_choice):
        """
        Validates the user's menu choice.
        """
        while True:
            if self.is_valid_menu_option(menu_choice):
                return menu_choice
            else:
                self.view.display_error(
                    "Veuillez choisir une option valide : 1, 2, 3, 4, 5 ou 0."
                )
                menu_choice = self.view.display_tournament_menu()

    def is_valid_menu_option(self, menu_choice):
        """
        Check if the menu choice is valid (i.e., one of '1', '2', '3', '4' '5' or '0').
        """
        return menu_choice in ["1", "2", "3", "4", "5", "0"]

    ############################################################################################################
    #                                                VALID NAME                                                #
    ############################################################################################################
    def validate_tournament_name(self, input_function):
        while True:
            name = input_function().strip()
            if self.is_valid_name(name):
                return name

    def is_valid_name(self, name):
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
    #                                                VALID LOCATION                                            #
    ############################################################################################################
    def validate_tournament_location(self, input_function):
        while True:
            location = input_function().strip()
            if self.is_valid_location(location):
                return location

    def is_valid_location(self, location):
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
    #                                               VALID DESCRIPTION                                          #
    ############################################################################################################
    def validate_tournament_description(self, input_function):
        while True:
            description = input_function().strip()
            if self.is_valid_description(description):
                return description

    def is_valid_description(self, description):
        if len(description) < 2 or len(description) > 200:
            self.view.display_error(
                "La description doit être entre 5 et 200 caractères !"
            )
            return False
        return True

    ############################################################################################################
    #                                               VALID START DATE                                           #
    ############################################################################################################
    def validate_tournament_start_date(self, input_function):
        while True:
            start_date = input_function().strip()
            if self.is_valid_start_date(start_date):
                return start_date

    def is_valid_start_date(self, date_str):
        try:
            datetime.strptime(date_str, "%d/%m/%Y %H:%M")
            return True
        except ValueError:
            self.view.display_error("Veuillez saisir une date au format 'dd/mm/YYYY' !")
            return False

    ############################################################################################################
    #                                                VALID END DATE                                            #
    ############################################################################################################
    def validate_tournament_end_date(self, input_function):
        while True:
            end_date = input_function().strip()
            if end_date == "" or self.is_valid_end_date(end_date):
                return end_date

    def is_valid_end_date(self, date_str):
        try:
            datetime.strptime(date_str, "%d/%m/%Y")
            return True
        except ValueError:
            self.view.display_error("Veuillez saisir une date au format 'dd/mm/YYYY' !")
            return False

    ############################################################################################################
    #                                           VALID REGISTRATION METHOD                                      #
    ############################################################################################################
    def validate_registration_method_choice(self, choice):
        while True:
            if self.is_valid_registration_method(choice):
                return choice
            else:
                self.view.display_error(
                    "Veuillez choisir une option valide : 1, 2, 3 ou 0."
                )
                choice = self.view.display_tournament_menu()

    def is_valid_registration_method(self, choice):
        """
        Check if the registration method choice is valid (i.e., one of '1', '2', or '0').
        """
        return choice in ["1", "2", "3", "0"]

    ############################################################################################################
    #                                             VALID PLAYER SELECTION                                       #
    ############################################################################################################
    def validate_selected_players_input(self, input_function, players):
        while True:
            selected_players = input_function(players).strip()
            if self.is_valid_player_selection(selected_players, players):
                return selected_players

    def is_valid_player_selection(self, selected_players, players):
        try:
            selected_players = [int(i) - 1 for i in selected_players.split()]
            for idx in selected_players:
                if idx < 0 or idx >= len(players):
                    self.view.display_error("Le joueur à cet index n'existe pas.")
                    return False
            return True
        except ValueError:
            self.view.display_error("Veuillez saisir des indices de joueurs valides.")
            return False
