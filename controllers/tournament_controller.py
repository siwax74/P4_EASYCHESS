from datetime import datetime
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

    def display_menu(self):
        """
        Displays the tournament menu and gets the user's choice.
        """
        choice = self.view.display_tournament_menu()
        self._process_choice(choice)

    def _process_choice(self, choice):
        """
        Processes the user's choice.
        """
        if choice == "1":
            self.create_tournament()
        elif choice == "2":
            self.display_tournament_list()
        elif choice == "3":
            self.display_tournaments()    
        elif choice == "0":
            print("Retour au menu principal...")
        else:
            self.view.display_error("Choix invalide")
            self.display_menu()

    def create_tournament(self):
        """
        Handles the tournament creation process.
        """
        tournament_info = self._get_tournament_info()
        if tournament_info is None:
            return

        name, location, start_date, end_date, rounds, description, players = tournament_info
        tournament = self._create_tournament(
            name, location, start_date, end_date, rounds, description, players)
        self.view.display_success("Le tournoi a été créé avec succès!")
        self._save_tournament(tournament)

    def _get_tournament_info(self):
        """
        Collects all necessary information to create a tournament.
        """
        name = self._get_name()
        if not name:
            return None

        location = self._get_location()
        if not location:
            return None

        start_date = self._get_start_date()
        if not start_date:
            return None

        end_date = self._get_end_date()
        if not end_date:
            return None

        rounds = self._get_rounds()
        description = self._get_description()

        players = self._get_players()
        if not players:
            return None

        return name, location, start_date, end_date, rounds, description, players

    def _get_name(self):
        """
        Gets the tournament name from the user.
        """
        return self._get_valid_input(self.view.ask_name, "Le nom est obligatoire")

    def _get_location(self):
        """
        Gets the tournament location from the user.
        """
        return self._get_valid_input(self.view.ask_location, "Le lieu est obligatoire")

    def _get_start_date(self):
        """
        Gets a valid start date from the user.
        """
        return self._get_valid_date(self.view.ask_start_date)

    def _get_end_date(self):
        """
        Gets a valid end date from the user.
        """
        return self._get_valid_date(self.view.ask_end_date)

    def _get_rounds(self):
        """
        Gets the number of rounds from the user.
        """
        return self.view.ask_rounds() or 4

    def _get_description(self):
        """
        Gets a description for the tournament from the user.
        """
        return self.view.ask_description()

    def _get_players(self):
        """
        Handles the player selection for the tournament.
        """
        return self._select_players()

    def _get_valid_input(self, input_function, error_message):
        """
        General function to get a valid input.
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
        General function to get a valid date.
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
        Validates the provided date string.
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
        Manages player selection for the tournament.
        """
        registration_method = self.view.ask_player_registration()
        if registration_method == "a":
            return self._get_all_players()

        return self._choose_specific_players()

    def _get_all_players(self):
        """
        Loads and returns all available players from the database.
        """
        return load_from_json(self.file_player)

    def _choose_specific_players(self):
        """
        Handles the process of choosing specific players.
        """
        players = load_from_json(self.file_player)
        if not players:
            self.view.display_error("Aucun joueur disponible.")
            return []
        self._display_players(players)
        selected_players = self._process_player_selection(players)
        return selected_players

    def _display_players(self, players):
        """
        Displays the list of available players.
        """
        for i, (key, player) in enumerate(players.items(), start=1):
            print(f"{i}. {player['first_name']} {player['last_name']} (ID: {key})")

    def _process_player_selection(self, players):
        """
        Processes player selection from the user.
        """
        selections = self.view.ask_player_selection()
        if selections is None:
            self.view.display_error("Sélection des joueurs annulée.")
            return None
        selected_indices = self._parse_player_selection(selections)
        return self._get_selected_players(selected_indices, players)

    def _parse_player_selection(self, selections):
        """
        Parses and validates player selection input.
        """
        try:
            return [int(x.strip()) for x in selections.split(",")]
        except ValueError:
            self.view.display_error("Entrée non valide. Veuillez entrer des numéros séparés par des virgules.")
            return []

    def _get_selected_players(self, selected_indices, players):
        """
        Retrieves the selected players based on indices.
        """
        selected_players = {}
        for index in selected_indices:
            if 1 <= index <= len(players):
                key = list(players.keys())[index - 1]
                selected_players[f"player{index}"] = players[key]      
            else:
                self.view.display_error(f"Le numéro {index} est invalide.")
        return selected_players

    def _create_tournament(self, name, location, start_date, end_date, number_of_rounds, description, players):
        """
        Creates a new Tournament object.
        """
        return Tournament(name, location, start_date, end_date, number_of_rounds, description, players)

    def _save_tournament(self, tournament):
        """
        Saves the tournament to the database.
        """
        set_tournament_to_json(tournament.as_dict(), self.file_tournament)

    def _get_all_tournaments(self):
        return load_from_json(self.file_tournament)
         
    def display_tournaments(self):
        try:
            tournaments = self._get_all_tournaments()
            choice = self.view.display_tournaments(tournaments)
            return self.choice_list_tournaments(choice, tournaments)
        except Exception as e:
            self.view.display_error("Erreur lors de la récupération des tournois")
            self.view.display_menu()
            return None
            
    def choice_list_tournaments(self, choice, tournaments):
        if choice == "1":
            return self.ask_choosen_tournament(tournaments)
        elif choice == "0":
            self.view.display_menu()
            return None
        else:
            self.view.display_error("Sélection invalide")
            return None

    def ask_choosen_tournament(self, tournaments):
        choosen_tournament_name = self.view.ask_name() #On récupère la méthodes ask_
        return self.get_start_tournament(choosen_tournament_name, tournaments)
    
    def get_start_tournament(self, choosen_tournament_name, tournaments):
        for tournament_id in tournaments:
            if tournament_id == choosen_tournament_name:
                return self.ask_confirmation_start(choosen_tournament_name)
            
    def ask_confirmation_start(self, choosen_tournament_name):
        choice = self.view.ask_confirmation_start_tournament(choosen_tournament_name)
        return self.start_tournament(choice, choosen_tournament_name)
    
    def start_tournament(self, choice, choosen_tournament_name):
        if choice == "":
            print(f"Demarrage du tournois,{choosen_tournament_name}")

    