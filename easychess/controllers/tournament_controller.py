from datetime import datetime
import math
import random
from settings import TOURNAMENTS_FILE, PLAYERS_FILE
from .player_controller import PlayerManagerController
from ..models.player import Player
from ..models.round import Round
from ..models.match import Match
from ..models.tournament import Tournament
from ..utils.sanitize import Sanitize
from ..utils.tournament_validator import TournamentInputValidator
from ..views.tournament_view import TournamentView


class TournamentManagerController:
    """
    Controller class for managing tournaments.
    """

    def __init__(self):
        """
        Controller class for managing tournaments.

        Attributes:
            view (TournamentView): The view object for displaying tournament information.
            file_tournament (str): The file path for storing tournament data.
            file_player (str): The file path for storing player data.
            value_validator (TournamentValidator): The validator object for validating tournament values.
            input_validator (InputValidator): The validator object for validating user input.
        """
        self.view = TournamentView()
        self.file_tournament = TOURNAMENTS_FILE
        self.file_player = PLAYERS_FILE
        self.sanitize = Sanitize(self.view)
        self.input_validator = TournamentInputValidator(self.view, self.file_player, self.sanitize)

    def show_menu_options(self):
        """
        Initializes the controller with a view and file paths.

        Args:
            None

        Returns:
            None
        """
        while True:
            menu_choice = self.view.display_tournament_menu()
            valid_choice = self.input_validator.validate_menu_choice(menu_choice)
            if valid_choice == "1":
                new_tournament = self.create_tournament(valid_choice)
                print(new_tournament)
                self.start_tournament(new_tournament)
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
        """Creates a new tournament."""
        if not choice:
            return False
        tournament_infos = self.gather_tournament_information()
        if not tournament_infos:
            return False
        new_tournament = Tournament.create(tournament_infos)
        players_registration_method = self.choose_players_registration_method(new_tournament)
        if not players_registration_method:
            return False
        initiate_tournament = self.generate_tournament(new_tournament)
        if initiate_tournament == "0":
            return False
        self.view.display_success("Génération du tournoi réussie !")
        return new_tournament

    def generate_tournament(self, new_tournament):
        """Gère le lancement du tournoi."""
        choice = self.input_validator.validate_input(self.view.ask_start_tournament)
        if choice == "o":
            list_rounds = self.generate_rounds(new_tournament)
            self.generate_matches(new_tournament, list_rounds[0])
            return new_tournament
        return choice if choice == "0" else None

    def generate_rounds(self, new_tournament):
        """Génère les rounds nécessaires."""
        num_players = len(new_tournament.players)
        num_rounds = max(4, math.ceil(math.log2(num_players)))
        new_tournament.number_of_rounds = num_rounds
        list_rounds = []
        for i in range(1, num_rounds + 1):
            round_name = f"Round {i}"
            round_obj = Round.create(round_name)
            list_rounds.append(round_obj)
            new_tournament.list_rounds.append(round_obj)
        return list_rounds

    def generate_matches(self, new_tournament, round):
        """Génère des paires de joueurs pour un round."""
        players = new_tournament.players
        if len(players) < 2:
            raise ValueError("Pas assez de joueurs pour créer des matchs.")
        random.shuffle(players)
        sorted_players = sorted(players, key=lambda x: x.get("score"), reverse=True)
        round.matches = []
        while len(sorted_players) >= 2:
            player1, player2 = sorted_players.pop(0), sorted_players.pop(0)
            match = Match.create(player1, player2)
            round.add_match(match)

    def start_tournament(self, new_tournament):
        """Gère le déroulement du tournoi."""
        new_tournament.start_date = datetime.now()
        for round_index in range(new_tournament.number_of_rounds):
            round = new_tournament.list_rounds[round_index]
            self.play_round(round, round_index)
            if round_index < new_tournament.number_of_rounds - 1:
                self.prepare_next_round(new_tournament, round_index)
            else:
                self.end_tournament(new_tournament)
        Tournament.save(self.file_tournament, new_tournament.as_dict())

    def play_round(self, round, round_index):
        """Joue un round du tournoi."""
        for match_index, match in enumerate(round.matches):
            self.view.display(round, round_index)
            self.play_match(match, match_index)
        round.end_date_time = datetime.now()

    def play_match(self, match, match_index):
        """Joue un match et met à jour les scores."""
        ask_winner_match = self.input_validator.validate_match(self.view.ask_validate_match(match, match_index))
        if ask_winner_match == "1":
            match.set_score(1, 0)
            match.player1["score"] += 1
        elif ask_winner_match == "2":
            match.set_score(0, 1)
            match.player2["score"] += 1
        elif ask_winner_match == "0":
            match.set_score(0.5, 0.5)
            match.player1["score"] += 0.5
            match.player2["score"] += 0.5

    def prepare_next_round(self, new_tournament, round_index):
        """Prépare le prochain round."""
        self.view.display_success("Tour suivant...")
        self.generate_matches(new_tournament, new_tournament.list_rounds[round_index + 1])

    def end_tournament(self, new_tournament):
        """Termine le tournoi."""
        new_tournament.end_date = datetime.now()
        self.view.display_success("Fin du tournoi !")

    def gather_tournament_information(self):
        """
        Gathers information for creating a new tournament.
        """
        while True:
            name = self.input_validator.validate_name(self.view.ask_name)
            if name is False:
                break
            location = self.input_validator.validate_location(self.view.ask_location)
            if location is False:
                break
            description = self.input_validator.validate_description(self.view.ask_description)
            if description is False:
                break
            tournament_info = name, location, description
            return tournament_info

    def choose_players_registration_method(self, new_tournament):
        while True:
            choice_players_registration_method = self.view.ask_player_registration_method()
            valid_method = self.input_validator.validate_registration_method(choice_players_registration_method)
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

        ############################################################################################################
        #                                                 ADD PLAYERS AUTO                                         #
        ############################################################################################################

    def register_players_automatically(self, new_tournament):
        """
        Enregistre les joueurs automatiquement à partir d'un fichier et les ajoute au tournoi.
        """
        try:
            players = Player.read(self.file_player)
            new_tournament.players.extend(players)
            return new_tournament

        except Exception as e:
            raise Exception(f"Une erreur est survenue lors de l'enregistrement automatique des joueurs : {str(e)}")

        ############################################################################################################
        #                                                 ADD PLAYERS MANUALLY                                     #
        ############################################################################################################

    def register_players_manually(self, new_tournament):
        try:
            players = Player.read(self.file_player)
            selected_player_indices = self.input_validator.validate_selected_players(
                self.view.ask_player_selection, players
            )
            selected_player_indices = [int(i) - 1 for i in selected_player_indices.split()]
            for idx in selected_player_indices:
                if 0 <= idx < len(players):
                    player = players[idx]
                    new_tournament.players.append(player)
                else:
                    raise IndexError("Le joueur à cet index n'existe pas.")
            return new_tournament

        except Exception as e:
            raise Exception(f"Une erreur est survenue : {str(e)}")

        ############################################################################################################
        #                                    CREATE AND ADD PLAYERS IN TOURNAMENT                                  #
        ############################################################################################################

    def add_new_player(self, new_tournament):
        while True:
            self.player_manager_controller = PlayerManagerController()
            new_player = self.player_manager_controller.create_player()
            new_tournament.players.append(new_player.as_dict())
            add_another = self.input_validator.validate_input(self.view.ask_add_another_player)
            if add_another == "o":
                continue
            else:
                return new_player

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
        tournaments = Tournament.read(self.file_tournament)
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
            tournaments = Player.read(self.file_tournament)
            if not tournaments:
                self.view.display_error("Aucun tournois enregistré !")
                return
            in_progress_tournaments = self.filter_tournaments(tournaments, "in_progress")
            if not in_progress_tournaments:
                self.view.display_error("Aucun tournois a venir !")
                return
            tournament_data = self.prepare_tournament_data(in_progress_tournaments)
            self.view.display_tournament_list(tournament_data)
            go_menu = self.input_validator.validate_return_to_menu(self.view.ask_return_menu)
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
            "number_of_rounds": details.get("number_of_rounds", "Nombre de tours non disponible"),
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
                "birthdate": player.get("birthdate", "Date de naissance non disponible"),
                "national_id": player.get("national_id", "Identifiant national non disponible"),
            }
            player_details.append(player_info)
        return player_details
