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
            elif valid_choice == "2":
                self.get_tournament_by_name()
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
            if len(new_tournament.players) < 5:
                print("Erreur : Il doit y avoir au moins 5 joueurs pour démarrer le tournoi.")
                return None
            list_rounds = self.generate_rounds(new_tournament)
            self.generate_matches(new_tournament, list_rounds[0])
            return new_tournament
        return choice if choice == "0" else None

    def generate_rounds(self, new_tournament):
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
        players_sorted = self.sort_players_by_score(players_shuffle)
        self.create_matches(players_sorted, round, new_tournament)

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
        if len(players) < 5:
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

    def sort_players_by_score(self, players_shuffle):
        """
        Sorts players by their score in descending order.

        Args:
            players_shuffle (list): The shuffled list of players to sort.

        Returns:
            list: The sorted list of players.
        """
        players_sorted = sorted(players_shuffle, key=lambda x: x["score"], reverse=True)
        return players_sorted

    def create_matches(self, players_sorted, round, tournament):
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

        # Set pour suivre les joueurs qui ont déjà été appariés dans ce tour
        matched_players = set()

        # Liste des joueurs non appariés dans ce tour
        unpaired_players = players_sorted[:]

        i = 0  # indice pour parcourir la liste des joueurs

        while i < len(unpaired_players):  # tant que i est inférieur à la longueur de la liste des joueurs non appariés
            player1 = unpaired_players[i]

            # Si 'player1' est déjà apparié, passer au joueur suivant
            if player1["last_name"] in matched_players:
                i += 1
                continue

            # Tenter d'apparier 'player1' avec un adversaire
            matched = False
            for j in range(i + 1, len(unpaired_players)):
                player2 = unpaired_players[j]

                # Vérifier si les joueurs se sont déjà rencontrés
                if not self.have_players_met(player1, player2, tournament):
                    # Créer le match et ajouter les joueurs à la liste des appariés
                    print(f"Appariement réussi: {player1['last_name']} vs {player2['last_name']}")
                    match = Match.create(player1, player2)
                    round.add_match(match)
                    matched_players.add(player1["last_name"])
                    matched_players.add(player2["last_name"])

                    # Supprimer 'player2' de la liste des joueurs non appariés
                    unpaired_players.pop(j)
                    matched = True
                    break

            if not matched:
                # Si aucun appariement inédit n'a été trouvé, tenter d'autres stratégies avant d'appairer de force
                print(f"Pas d'adversaire inédit pour {player1['last_name']}, recherche plus large...")

                # Recherche élargie parmi les joueurs non appariés restants
                for k in range(i + 1, len(unpaired_players)):
                    player2 = unpaired_players[k]

                    # Si un joueur est disponible plus loin dans la liste
                    if player2["last_name"] not in matched_players:
                        print(
                            f"Appariement forcé: {player1['last_name']} avec {player2['last_name']}(recherche étendue)"
                        )
                        match = Match.create(player1, player2)
                        round.add_match(match)
                        matched_players.add(player1["last_name"])
                        matched_players.add(player2["last_name"])
                        unpaired_players.pop(k)
                        break
                else:
                    # Si même la recherche élargie échoue, forcer l'appariement avec le joueur suivant immédiat
                    if i + 1 < len(unpaired_players):
                        player2 = unpaired_players[i + 1]
                        print(f"Appariement forcé final: {player1['last_name']} avec {player2['last_name']}")
                        match = Match.create(player1, player2)
                        round.add_match(match)
                        matched_players.add(player1["last_name"])
                        matched_players.add(player2["last_name"])

            # Passer au joueur suivant
            i += 1

        # Gérer le cas où le nombre de joueurs est impair
        if len(unpaired_players) % 2 != 0:
            last_player = unpaired_players[-1]
            if last_player["last_name"] not in matched_players:
                self.handle_odd_player(last_player)

    def have_players_met(self, player1, player2, tournament):
        """
        Checks if two players have already faced each other in the tournament.

        Args:
            player1 (dict): The first player.
            player2 (dict): The second player.
            tournament (Tournament): The tournament to check against.

        Returns:
            bool: True if the players have met, False otherwise.
        """
        for round in tournament.list_rounds:
            for match in round.matches:
                if (
                    match.player1["last_name"] == player1["last_name"]
                    and match.player2["last_name"] == player2["last_name"]
                ) or (
                    match.player1["last_name"] == player2["last_name"]
                    and match.player2["last_name"] == player1["last_name"]
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
        if not new_tournament:
            return False

        new_tournament.status = True
        new_tournament.start_date = datetime.now()

        print(f"Début du tournoi: {new_tournament.name}")
        print(f"Nombre de rounds: {new_tournament.number_of_rounds}")
        print(f"Round actuel: {new_tournament.current_round}")
        time.sleep(1)

        while new_tournament.current_round < new_tournament.number_of_rounds:
            print(f"Jouer round {new_tournament.current_round}/{new_tournament.number_of_rounds}")

            round = new_tournament.list_rounds[new_tournament.current_round]

            # Générer des matchs si pas encore généré
            if not round.matches:
                self.generate_matches(new_tournament, round)
                print(f"Matchs générés pour le round {new_tournament.current_round}")

            # Jouer le round actuel
            self.play_round(round, new_tournament, new_tournament.current_round)

            # Préparer le prochain round
            if not self.prepare_next_round(new_tournament):
                print(f"Le tournoi s'arrête au round {new_tournament.current_round}")
                new_tournament.status = None
                self.end_tournament(new_tournament)
                return False

        self.end_tournament(new_tournament)
        return True

    def play_round(self, round, new_tournament, round_index):
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
        new_tournament.current_round += 1

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

    def prepare_next_round(self, new_tournament):
        if new_tournament.current_round >= new_tournament.number_of_rounds:
            new_tournament.status = True
            self.end_tournament(new_tournament)
            return False

        next_round_input = self.input_validator.validate_input(self.view.ask_next_round)
        if next_round_input == "o":
            if new_tournament.current_round <= new_tournament.number_of_rounds:
                self.utils.display_success("Tour suivant...")
                if not new_tournament.list_rounds[new_tournament.current_round].matches:
                    self.generate_matches(new_tournament, new_tournament.list_rounds[new_tournament.current_round])
            else:
                # Si c'est le dernier round, jouer les matchs sans incrémenter le round
                self.utils.display_success("Dernier tour...")
                if not new_tournament.list_rounds[new_tournament.current_round].matches:
                    self.generate_matches(new_tournament, new_tournament.list_rounds[new_tournament.current_round])
            return True
        elif next_round_input == "n":
            self.utils.display_success("Retour au menu principal...")
            return False

    def end_tournament(self, new_tournament):
        """
        Ends the tournament, finalizing the results and cleaning up.

        Args:
            new_tournament (Tournament): The tournament that is being ended.
        """
        new_tournament.end_date = datetime.now()
        Tournament.save(self.db_tournament, new_tournament.as_dict())
        self.utils.display_success("Fin du tournoi !")

    def get_tournament_by_name(self):
        """
        Retrieves and displays details of tournaments with 'None' status.

        The method retrieves all tournaments, filters the ones with a 'None' status,
        and displays their details. If a tournament name is found, it attempts to start that tournament.
        """
        tournaments = Tournament.read(self.db_tournament)
        none_status_tournaments = {
            key + 1: tournament
            for key, tournament in enumerate(tournaments.items())
            if tournament[1].get("status") is None
        }
        if not none_status_tournaments:
            self.utils.display_success("Aucun tournois en cour ! ")
            return
        self.view.display_tournaments_name(none_status_tournaments)
        tournament_index = self.input_validator.validate_tournament_index(
            self.view.ask_tournament_name_input, none_status_tournaments
        )
        if tournament_index in none_status_tournaments:
            self.transform_to_obj(tournament_index, none_status_tournaments)

    def transform_to_obj(self, tournament_index, none_status_tournaments):
        selected_tournament = none_status_tournaments[tournament_index]
        tournament = Tournament(**selected_tournament[1])
        rounds = []
        for round_dict in tournament.list_rounds:
            round = Round(**round_dict)
            round.matches = [Match.from_tuple(match) for match in round_dict["matches"]]
            rounds.append(round)
        tournament.list_rounds = rounds
        self.start_tournament(tournament)
