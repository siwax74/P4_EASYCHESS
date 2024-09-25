from datetime import datetime
import random
import time
from easychess.controllers.player_controller import PlayerManagerController
from easychess.models.match import Match
from easychess.models.player import Player
from easychess.models.round import Round
from easychess.models.tournament import Tournament
from easychess.utils.sanitize import Sanitize
from easychess.utils.tournament_validator import TournamentInputValidator
from easychess.utils.utils import Utils
from easychess.views.tournament_view import TournamentView
from settings import TOURNAMENTS_FILE, PLAYERS_FILE


class TournamentManagerController:
    """
    Controller class for managing tournaments, including creating, starting,
    and managing rounds and matches.
    """

    def __init__(self):
        """
        Initializes the TournamentManagerController with the required views,
        file paths, and utility objects for managing tournament data.

        Attributes:
            view (TournamentView): The view object for displaying tournament information.
            db_tournament (str): The file path for storing tournament data.
            db_player (str): The file path for storing player data.
            sanitize (Sanitize): The sanitizer object for input sanitization.
            input_validator (TournamentInputValidator): The validator object for validating user input.
        """
        self.view = TournamentView()
        self.db_tournament = TOURNAMENTS_FILE
        self.db_player = PLAYERS_FILE
        self.utils = Utils()
        self.sanitize = Sanitize(self.view)
        self.input_validator = TournamentInputValidator(self.utils, self.db_player, self.sanitize)

    def show_menu_options(self):
        """
        Displays the main menu options for tournament management and handles
        user choices for creating and starting tournaments.
        """
        while True:
            menu_choice = self.view.display_tournament_menu()
            valid_choice = self.input_validator.validate_menu_choice(menu_choice)
            if valid_choice == "1":
                new_tournament = self.create_tournament(valid_choice)
                self.start_tournament(new_tournament)
            elif valid_choice == "0":
                break

    def create_tournament(self, choice):
        """
        Creates a new tournament by gathering tournament information and registering players.

        Args:
            choice (str): User choice for tournament creation.

        Returns:
            Tournament: The newly created tournament object or False if creation fails.
        """
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
        if initiate_tournament is None:
            return False
        
        self.utils.display_success("Génération du tournoi réussie !")
        return new_tournament

    def gather_tournament_information(self):
        """
        Gathers information necessary to create a new tournament from user input.

        Returns:
            tuple: A tuple containing the tournament name, location, and description or False if invalid.
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
        """
        Allows the user to choose a method for registering players to the tournament.

        Args:
            new_tournament (Tournament): The tournament for which players are being registered.

        Returns:
            bool: True if players are registered successfully, False otherwise.
        """
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

    def register_players_automatically(self, new_tournament):
        """
        Automatically registers players from a file and adds them to the tournament.

        Args:
            new_tournament (Tournament): The tournament to which players will be added.

        Returns:
            Tournament: The tournament with players added.

        Raises:
            Exception: If an error occurs during automatic registration.
        """
        try:
            players = Player.read(self.db_player)
            new_tournament.players.extend(players)
            return new_tournament
        except Exception as e:
            raise Exception(f"Une erreur est survenue lors de l'enregistrement automatique des joueurs : {str(e)}")

    def register_players_manually(self, new_tournament):
        """
        Allows the user to manually select players to add to the tournament.

        Args:
            new_tournament (Tournament): The tournament to which players will be added.

        Returns:
            Tournament: The tournament with players added.

        Raises:
            IndexError: If a selected player index does not exist.
            Exception: If an error occurs during manual registration.
        """
        try:
            players = Player.read(self.db_player)
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

    def add_new_player(self, new_tournament):
        """
        Adds a new player to the tournament.

        Args:
            new_tournament (Tournament): The tournament to which the new player will be added.

        Returns:
            Player: The newly added player.
        """
        while True:
            self.player_manager_controller = PlayerManagerController()
            new_player = self.player_manager_controller.create_player()
            new_tournament.players.append(new_player.as_dict())
            add_another = self.input_validator.validate_add_new_player(self.view.ask_add_another_player)
            if add_another == "o":
                continue
            else:
                return new_player

    def generate_tournament(self, new_tournament):
        """
        Manages the initiation of the tournament.

        Args:
            new_tournament (Tournament): The tournament object to be initiated.

        Returns:
            Tournament: The initiated tournament object or None if not started.
        """
        choice = self.input_validator.validate_input(self.view.ask_start_tournament)
        if choice == "o":
            if len(new_tournament.players) < 2:
                print("Erreur : Il doit y avoir au moins 2 joueurs pour démarrer le tournoi.")
                return None
            list_rounds = self.generate_rounds(new_tournament)
            self.generate_matches(new_tournament, list_rounds[0])
            return new_tournament
        return choice if choice == "0" else None
    
    def generate_rounds(self, new_tournament):
        """
        Generates the necessary rounds for the tournament based on the number of players.

        Args:
            new_tournament (Tournament): The tournament for which rounds are generated.

        Returns:
            list: A list of Round objects created for the tournament.
        """
        num_players = len(new_tournament.players)
        num_rounds = num_players - 1
        new_tournament.number_of_rounds = num_rounds
        list_rounds = []
        for i in range(1, num_rounds + 1):
            round_name = f"Round {i}"
            round_obj = Round.create(round_name)
            list_rounds.append(round_obj)
            new_tournament.list_rounds.append(round_obj)
        return list_rounds

    def generate_matches(self, new_tournament, round):
        """
        Generates player pairs for a round of the tournament.

        Args:
            new_tournament (Tournament): The tournament for which matches are generated.
            round (Round): The current round for which matches are to be created.
        """
        players = self.get_players(new_tournament)
        players_shuffle = self.shuffle_players(players)
        self.create_matches(players_shuffle, round, new_tournament)

    def get_players(self, new_tournament):
        """
        Retrieves the players registered in the tournament.

        Args:
            new_tournament (Tournament): The tournament from which to get players.

        Returns:
            list: The list of players participating in the tournament.

        Raises:
            ValueError: If there are not enough players to create matches.
        """
        players = new_tournament.players
        if len(players) < 2:
            raise ValueError("Pas assez de joueurs pour créer des matchs.")
        return players

    def shuffle_players(self, players):
        """
        Randomly shuffles the list of players.

        Args:
            players (list): The list of players to shuffle.

        Returns:
            list: The shuffled list of players.
        """
        random.shuffle(players)
        return players

    def create_matches(self, players_shuffle, round, tournament):
        """
        Crée les matches pour un tour du tournoi tout en évitant les rencontres répétées si possible.
        Si aucun match inédit n'est possible, un appariement forcé est fait.

        Args:
            players_sorted (list): La liste triée des joueurs à apparier pour les matches.
            round (Round): Le tour actuel pour lequel les matches sont créés.
            tournament (Tournament): Le tournoi auquel appartiennent les matches.
        """
        # Initialiser la liste des matches pour ce tour
        round.matches = []
        players_set = set()
        for i in range(0, len(players_shuffle)):
            player1 = players_shuffle[i]
            if player1["last_name"] in players_set:
                continue
            player2 = self.get_player2(player1, players_shuffle, players_set, tournament)
            if player2:
                match = Match(player1, player2)
                round.add_match(match)
                players_set.add(player1["last_name"])
                players_set.add(player2["last_name"])
            else:
                print("ok forcage")
    def get_player2(self, player1, players_shuffle, players_set, tournament):
        """
        Trouve un adversaire pour player1 tout en évitant les matchs répétés.

        Args:
            player1 (dict): Le joueur pour lequel on cherche un adversaire.
            players_shuffle (list): Liste mélangée des joueurs pour le tour actuel.
            players_set (set): Ensemble des joueurs déjà utilisés dans les matchs du tour actuel.
            tournament (Tournament): L'objet tournoi contenant tous les tours et matchs précédents.

        Returns:
            dict: Un joueur à apparier avec player1 ou None si aucun joueur disponible.
        """
        random.shuffle(players_shuffle)
        for player2 in players_shuffle:
            if player2["last_name"] in players_set or player1["last_name"] == player2["last_name"]:
                continue
            # Vérifier si player1 et player2 se sont déjà affrontés
            if not self.have_players_met(player1, player2, tournament):
                return player2
        return None

    def have_players_met(self, player1, player2, tournament):
        """
        Vérifie si deux joueurs se sont déjà affrontés dans le tournoi.

        Args:
            player1 (dict): Le premier joueur.
            player2 (dict): Le second joueur.
            tournament (Tournament): Le tournoi dans lequel vérifier les matchs.

        Returns:
            bool: True si les joueurs se sont déjà rencontrés, False sinon.
        """
        for round in tournament.list_rounds:
            for match in round.matches:
                if (
                    (match.player1["last_name"] == player1["last_name"] and match.player2["last_name"] == player2["last_name"])
                    or (match.player1["last_name"] == player2["last_name"] and match.player2["last_name"] == player1["last_name"])
                ):
                    return True
        return False

    def handle_odd_player(self, player):
        """
        Handles the situation of having an odd number of players.

        Args:
            player (dict): The player without an opponent.
        """
        player["score"] += 0.5
        self.utils.display_success(f"{player['last_name']} {player['first_name']} a un bye et marque 0,5 point.")

    def start_tournament(self, new_tournament):
        """
        Manages the flow of the tournament, including starting rounds and playing matches.

        Args:
            new_tournament (Tournament): The tournament to be started.

        Returns:
            bool: True if the tournament starts successfully, False otherwise.
        """
        if not new_tournament:
            return False
        new_tournament.start_date = datetime.now()
        for round_index in range(new_tournament.number_of_rounds):
            round = new_tournament.list_rounds[round_index]
            self.play_round(round, round_index)
            if round_index < new_tournament.number_of_rounds - 1:
                self.prepare_next_round(new_tournament, round_index)
            else:
                self.end_tournament(new_tournament)
        Tournament.save(self.db_tournament, new_tournament.as_dict())

    def play_round(self, round, round_index):
        """
        Plays a round of the tournament, managing individual matches.

        Args:
            round (Round): The round to be played.
            round_index (int): The index of the round in the tournament.
        """
        for match_index, match in enumerate(round.matches):
            self.view.display(round, round_index)
            self.play_match(match, match_index)
        round.end_date_time = datetime.now()

    def play_match(self, match, match_index):
        """
        Plays a match and updates the scores based on the winner.

        Args:
            match (Match): The match to be played.
            match_index (int): The index of the match in the round.
        """
        while True:
            ask_winner_match = self.input_validator.validate_match(self.view.ask_validate_match(match, match_index))
            if ask_winner_match:
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
                break

    def prepare_next_round(self, new_tournament, round_index):
        """
        Prepares for the next round of the tournament.

        Args:
            new_tournament (Tournament): The tournament for which the next round is prepared.
            round_index (int): The index of the current round.
        """
        self.utils.display_success("Tour suivant...")
        self.generate_matches(new_tournament, new_tournament.list_rounds[round_index + 1])

    def end_tournament(self, new_tournament):
        """
        Ends the tournament, finalizing the results and cleaning up.

        Args:
            new_tournament (Tournament): The tournament that is being ended.
        """
        new_tournament.end_date = datetime.now()
        for player in new_tournament.players:
            if "opponents" in player:
                del player["opponents"]
        self.utils.display_success("Fin du tournoi !")
