from datetime import datetime
import re
import time
import unicodedata
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
        self.value_validator = TournamentValueValidator(self.view)
        self.input_validator = TournamentInputValidator(self.view, self.file_player, self.value_validator)

    def show_menu_options(self):
        """
        Displays the tournament menu and gets the user's choice.
        """
        while True:
            menu_choice = self.view.display_tournament_menu()
            valid_choice = self.input_validator.validate_choice_menu(menu_choice)
            if valid_choice == "1":
                self.create_tournament(valid_choice)
            elif valid_choice == "2":
                self.display_all_tournaments_upcoming()
            elif valid_choice == "3":
                self.display_all_tournaments_in_progress()
            elif valid_choice == "0":
                break
    ############################################################################################################
    #                                                 GET CHOICE MENU OPTION 1                                 #
    ############################################################################################################
    def create_tournament(self, choice):
        if choice:
            tournament_infos = self.gather_tournament_information()
            if not tournament_infos:
                return False
            new_tournament = Tournament.create(tournament_infos)
            players_registration_method  = self.choose_players_registration_method(new_tournament)
            if not players_registration_method:
                return False
            Tournament.save(self.file_tournament, new_tournament.as_dict())
            self.view.display_success("Tournois crée avec succès ! ")

    def gather_tournament_information(self):
        """
        Gathers information for creating a new tournament.
        """
        while True:
            name = self.input_validator.validate_tournament_name(self.view.ask_name)
            if name is False:
                break
            location = self.input_validator.validate_tournament_location(
                self.view.ask_location
            )
            if location is False:
                break
            start_date = self.input_validator.validate_tournament_start_date(
                self.view.ask_start_date
            )
            if start_date is False:
                break            
            end_date = self.input_validator.validate_tournament_end_date(
                self.view.ask_end_date
            )
            if end_date is False:
                break
            description = self.input_validator.validate_tournament_description(
                self.view.ask_description
            )
            if description is False:
                break
            tournament_info = name, location, start_date, end_date, description
            return tournament_info

    def choose_players_registration_method(self, new_tournament):
        while True:
            choice_players_registration_method = self.view.ask_player_registration_method()
            valid_method = self.input_validator.validate_registration_method_choice(choice_players_registration_method)
            if valid_method == "0":
                break
            elif valid_method == "1":
                players_add_auto = self.register_players_automatically(new_tournament)
                return players_add_auto
            elif valid_method == "2":
                players_add_manually = self.register_players_manually(new_tournament)
                return players_add_manually
            elif valid_method == "3":
                new_player = self.add_new_player(new_tournament)
                return new_player
            
    def add_new_player(self, new_tournament):
        while True:
            self.player_manager_controller = PlayerManagerController()
            new_player = self.player_manager_controller.create_player()
            new_tournament.players.append(new_player)
            print(new_tournament)
            add_another = self.input_validator.validate_input(
                        self.view.ask_add_another_player
                    )
            if add_another == "o":
                continue
            else:
                return new_player
        ############################################################################################################
        #                                                 ADD PLAYERS AUTO                                         #
        ############################################################################################################

    def register_players_automatically(self, new_tournament):
        """
        Registers players automatically from the file.
        """
        players = Player.read(self.file_player)
        players_add = Tournament.add_players_auto(players, new_tournament)
        return players_add
    
        ############################################################################################################
        #                                                 ADD PLAYERS MANUALLY                                     #
        ############################################################################################################

    def register_players_manually(self, new_tournament):
        players = Player.read(self.file_player)
        selected_player_indices = self.input_validator.validate_selected_players_input(
            self.view.ask_player_selection, players
        )
        tournament_players = Tournament.add_players_manually(
            selected_player_indices, players, new_tournament)
        return tournament_players

    ############################################################################################################
    #                                                 READ TOURNAMENT/PLAYERS                                  #
    ############################################################################################################
    def read_tournaments(self):
        """
        Reads existing tournaments from file.
        """
        return Tournament.read(self.file_tournament)

    ############################################################################################################
    #                                          GET CHOICE MENU OPTION 2                                        #
    ############################################################################################################
    ############################################################################################################
    #                                           DISPLAY UPCOMING                                              #
    ############################################################################################################
    def display_all_tournaments_upcoming(self):
        """
        Prepares data to display the list of upcoming tournaments.
        """
        tournaments = self.read_tournaments()
        if not tournaments:
            self.view.display_error("Aucun tournois enregistré !")
            return self.show_menu_options()
        upcoming_tournaments = self.filter_tournaments(tournaments, "upcoming")
        if not upcoming_tournaments:
            self.view.display_error("Aucun tournois a venir !")
            return self.show_menu_options()
        tournament_data = self.prepare_tournament_data(upcoming_tournaments)
        self.view.display_tournament_list(tournament_data)
        ############################################################################################################
        #                                          DISPLAY IN_PROGRESS                                             #
        ############################################################################################################

    def display_all_tournaments_in_progress(self):
        """
        Prepares data to display the list of in_progress tournaments.
        """
        while True:
            tournaments = self.read_tournaments()
            if not tournaments:
                self.view.display_error("Aucun tournois enregistré !")
                return
            in_progress_tournaments = self.filter_tournaments(tournaments, "in_progress")
            if not in_progress_tournaments:
                self.view.display_error("Aucun tournois a venir !")
                return
            tournament_data = self.prepare_tournament_data(in_progress_tournaments)
            self.view.display_tournament_list(tournament_data)
            go_menu = self.input_validator.validate_return_to_menu(
                self.view.ask_return_menu
            )
            if go_menu:
                break

        ############################################################################################################
        #                                          PREPARE DATA FOR DISPLAY VIEW                                   #
        ############################################################################################################

    def filter_tournaments(self, tournaments, status):
        """
        Filters tournaments based on their status.
        """
        return {
            tournament_id: details
            for tournament_id, details in tournaments.items()
            if details and details.get(status, True)
        }

    def prepare_tournament_data(self, upcoming_tournaments):
        """
        Prepares tournament data for display.
        """
        tournament_data = []
        for tournament_id, details in upcoming_tournaments.items():
            tournament_info = self.prepare_tournament_info(tournament_id, details)
            player_details = self.prepare_player_details(tournament_info["players"])
            tournament_info["player_details"] = player_details
            tournament_data.append(tournament_info)
        return tournament_data

    def prepare_tournament_info(self, tournament_id, details):
        """
        Prepares tournament information for display.
        """
        return {
            "id": tournament_id,
            "name": details.get("name", "Nom non disponible"),
            "location": details.get("location", "Emplacement non disponible"),
            "start_date": details.get("start_date", "Date de début non disponible"),
            "end_date": details.get("end_date", "Date de fin non disponible"),
            "number_of_rounds": details.get(
                "number_of_rounds", "Nombre de tours non disponible"
            ),
            "players": details.get("players", []),
            "current_round": details.get("current_round", "Tour actuel non disponible"),
            "list_rounds": details.get("list_rounds", []),
            "description": details.get("description", "Description non disponible"),
        }

    def prepare_player_details(self, players):
        """
        Prepares player details for display.
        """
        player_details = []
        for player in players:
            player_info = {
                "last_name": player.get("last_name", "Nom de famille non disponible"),
                "first_name": player.get("first_name", "Prénom non disponible"),
                "birthdate": player.get(
                    "birthdate", "Date de naissance non disponible"
                ),
                "national_id": player.get(
                    "national_id", "Identifiant national non disponible"
                ),
            }
            player_details.append(player_info)
        return player_details

############################################################################################################
#  VALUE VALIDATOR                                                                                         #
############################################################################################################
class TournamentValueValidator:
    def __init__(self, view):
        self.view = view

    def validate_players(self, tournament_info):
        players = tournament_info["players"]
        if players:
            return players
        else:
            self.view.display_error("No players found")

    def validate_count_players(self, players):
        count_players = len(players)
        return count_players
    
    def sanitize_text(self, text):
        """
        Replace accented characters with their non-accented counterparts.
        """
        accents = {
            'é': 'e', 'è': 'e', 'à': 'a', 'ù': 'u', 'ç': 'c', 'â': 'a', 'ê': 'e',
            'î': 'i', 'ô': 'o', 'û': 'u', 'ä': 'a', 'ë': 'e', 'ï': 'i', 'ö': 'o',
            'ü': 'u', 'ÿ': 'y'
        }
        for accented, non_accented in accents.items():
            text = text.replace(accented, non_accented)
        return text

############################################################################################################
#  INPUT VALIDATOR                                                                                         #
############################################################################################################
class TournamentInputValidator:
    def __init__(self, view, file_player, value_validator):
        self.view = view
        self.file_player = file_player
        self.value_validator = value_validator

    ############################################################################################################
    #                                                VALID MENU CHOICE                                         #
    ############################################################################################################
    def validate_choice_menu(self, choice):
        """
        Prompt and validate the user's choice.
        """
        if choice in ["0", "1", "2", "3", "4", "5"]:
            return choice
        else:
            self.view.display_error("Veuillez saisir un choix entre 0, 1, 2, 3, 4 ou 5 !")
            return False
    ############################################################################################################
    #                                                VALID NAME                                                #
    ############################################################################################################
    def validate_tournament_name(self, input_function):
        pattern = "^[0A-Za-zÀ-ÖØ-öø-ÿ' -]+$"
        while True:
            name = input_function().strip()
            if len(name) < 1 or len(name) > 50:
                self.view.display_error("Veuillez saisir un nom valide !")
            elif not re.match(pattern, name):
                self.view.display_error("Le nom ne peut pas contenir de caractères spéciaux !")
            elif name == "0":
                return False    
            else:
                name_sanitized = self.value_validator.sanitize_text(name)
                return name_sanitized
    ############################################################################################################
    #                                                VALID LOCATION                                            #
    ############################################################################################################
    def validate_tournament_location(self, input_function):
        pattern = "^[,0-9A-Za-zÀ-ÖØ-öø-ÿ' -]+$"
        while True:
            location = input_function().strip()
            if len(location) < 1 or len(location) > 50:
                self.view.display_error("Veuillez saisir un lieu valide !")
            elif not re.match(pattern, location):
                self.view.display_error("Le lieu ne peut pas contenir de caractères spéciaux !")
            elif location == "0":
                return False
            else:
                location_sanitized = self.value_validator.sanitize_text(location)
                return location_sanitized
    ############################################################################################################
    #                                               VALID START DATE                                           #
    ############################################################################################################
    def validate_tournament_start_date(self, input_function):
        while True:
            start_date = input_function().strip()
            try:
                datetime.strptime(start_date, "%d/%m/%Y %H:%M")
                return start_date
            except ValueError:
                if start_date == "0":
                    return False
                self.view.display_error("Veuillez saisir une date au format 'dd/mm/YYYY' !")

    ############################################################################################################
    #                                                VALID END DATE                                            #
    ############################################################################################################
    def validate_tournament_end_date(self, input_function):
        while True:
            end_date = input_function().strip()
            if end_date == "":
                return end_date
            try:
                datetime.strptime(end_date, "%d/%m/%Y")
                return end_date
            except ValueError:
                if end_date == "0":
                    return False
                self.view.display_error("Veuillez saisir une date au format 'dd/mm/YYYY' !")
        
    ############################################################################################################
    #                                               VALID DESCRIPTION                                          #
    ############################################################################################################
    def validate_tournament_description(self, input_function):
        while True:
            description = input_function().strip()
            if len(description) < 5 or len(description) > 200:
                self.view.display_error("La description doit être entre 5 et 200 caractères !")
            elif description == "0":
                return False
            else:
                description_sanitized = self.value_validator.sanitize_text(description)
                return description_sanitized

    ############################################################################################################
    #                                           VALID REGISTRATION METHOD                                      #
    ############################################################################################################
    def validate_registration_method_choice(self, choice):
        while True:
            if choice in ["1", "2", "3", "0"]:
                return choice
            else:
                self.view.display_error(
                    "Veuillez choisir une option valide : 1, 2, 3 ou 0."
                )
                return False

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

    ############################################################################################################
    #                                             VALID INPUT   o/n                                            #
    ############################################################################################################

    def validate_input(self, input_function):
        while True:
            response = input_function().strip()
            if self.is_valid_input(response):
                return response
            else:
                self.view.display_error("Veuillez répondre par o ou n ! ")

    def is_valid_input(self, response):
        return response in ["o", "n"]
    
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
