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
            sanitize (Sanitize): The sanitizer object for input sanitization.
            input_validator (TournamentInputValidator): The validator object for validating user input.
        """
        self.view = TournamentView()
        self.file_tournament = TOURNAMENTS_FILE
        self.file_player = PLAYERS_FILE
        self.sanitize = Sanitize(self.view)
        self.input_validator = TournamentInputValidator(self.view, self.file_player, self.sanitize)

    def show_menu_options(self):
        """
        Displays the main menu options and handles user choices.
        """
        while True:
            menu_choice = self.view.display_tournament_menu()
            valid_choice = self.input_validator.validate_menu_choice(menu_choice)
            if valid_choice == "1":
                new_tournament = self.create_tournament(valid_choice)
                self.start_tournament(new_tournament)
            elif valid_choice == "2":
                self.display_all_tournaments_upcoming()
            elif valid_choice == "3":
                self.display_all_tournaments_in_progress()
            elif valid_choice == "0":
                break

    def create_tournament(self, choice):
        """
        Creates a new tournament.
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
        self.view.display_success("Génération du tournoi réussie !")
        return new_tournament

    def generate_tournament(self, new_tournament):
        """
        Gère le lancement du tournoi.
        """
        choice = self.input_validator.validate_input(self.view.ask_start_tournament)
        if choice == "o":
            list_rounds = self.generate_rounds(new_tournament)
            self.generate_matches(new_tournament, list_rounds[0])
            return new_tournament
        return choice if choice == "0" else None

    def generate_rounds(self, new_tournament):
        """
        Génère les rounds nécessaires.
        """
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

    def get_players(self, new_tournament):
        players = new_tournament.players
        if len(players) < 2:
            raise ValueError("Pas assez de joueurs pour créer des matchs.")
        return players
    
    def shuffle_players(self, players):
        random.shuffle(players)
        return players
    
    def sort_players_by_score(self, players_shuffle):
        players_sorted = sorted(players_shuffle, key=lambda x: x["score"], reverse=True)
        return players_sorted
    
    def generate_matches(self, new_tournament, round):
        """
        Génère des paires de joueurs pour un round.
        """
        players = self.get_players(new_tournament)
        players_shuffle = self.shuffle_players(players)
        players_sorted = self.sort_players_by_score(players_shuffle)
        self.create_matches(players_sorted, round, new_tournament)

    def create_matches(self, players_sorted, round, tournament):
        """
        Crée les matchs pour un round en évitant les rencontres répétées si possible.
        """
        round.matches = []
        matched_players = set()
        
        for i in range(0, len(players_sorted)):
            if i + 1 >= len(players_sorted):
                break
            
            player1 = players_sorted[i]
            
            # Chercher un adversaire que player1 n'a pas encore rencontré
            for j in range(i + 1, len(players_sorted)):
                player2 = players_sorted[j]
                if not self.have_players_met(player1, player2, tournament):
                    match = Match.create(player1, player2)
                    round.add_match(match)
                    matched_players.add(player1['last_name'])
                    matched_players.add(player2['last_name'])
                    players_sorted.pop(j)
                    break
            
            # Si aucun adversaire non rencontré n'est trouvé, prendre le suivant disponible
            if player1['last_name'] not in matched_players:
                player2 = players_sorted[i + 1]
                match = Match.create(player1, player2)
                round.add_match(match)
                matched_players.add(player1['last_name'])
                matched_players.add(player2['last_name'])
        
        # Gérer le cas d'un nombre impair de joueurs
        if len(players_sorted) % 2 != 0:
            last_player = players_sorted[-1]
            if last_player['last_name'] not in matched_players:
                self.handle_odd_player(last_player, round)

    def have_players_met(self, player1, player2, tournament):
        """
        Vérifie si deux joueurs se sont déjà rencontrés dans le tournoi.
        """
        for round in tournament.list_rounds:
            for match in round.matches:
                if (match.player1['last_name'] == player1['last_name'] and match.player2['last_name'] == player2['last_name']) or \
                   (match.player1['last_name'] == player2['last_name'] and match.player2['last_name'] == player1['last_name']):
                    return True
        return False

    def handle_odd_player(self, player, round):
        """
        Gère le cas d'un nombre impair de joueurs.
        """
        # Implémenter la logique pour gérer un joueur impair
        # Par exemple, attribuer un bye ou un match contre un "joueur virtuel"
        pass

    def start_tournament(self, new_tournament):
        """
        Gère le déroulement du tournoi.
        """
        if not new_tournament:
            return False
        new_tournament.start_date = datetime.now()
        for round_index in range(new_tournament.number_of_rounds):
            round = new_tournament.list_rounds[round_index]
            self.play_round(round, round_index)
            if round_index < new_tournament.number_of_rounds - 1:
                self.prepare_next_round(new_tournament, round_index)
                for player in new_tournament.players:
                    print(f"Player {player['last_name']}: Opponents = {player.get('opponents', set())}")
            else:
                self.end_tournament(new_tournament)
        Tournament.save(self.file_tournament, new_tournament.as_dict())

    def play_round(self, round, round_index):
        """
        Joue un round du tournoi.
        """
        for match_index, match in enumerate(round.matches):
            self.view.display(round, round_index)
            self.play_match(match, match_index)
        round.end_date_time = datetime.now()

    def play_match(self, match, match_index):
        """
        Joue un match et met à jour les scores.
        """
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

        match.player1.setdefault("opponents", set()).add(match.player2['last_name'])
        match.player2.setdefault("opponents", set()).add(match.player1['last_name'])
        print(f"Player 1 ({match.player1['last_name']}): Opponents = {match.player1.get('opponents', set())}")
        print(f"Player 2 ({match.player2['last_name']}): Opponents = {match.player2.get('opponents', set())}")

    def prepare_next_round(self, new_tournament, round_index):
        """
        Prépare le prochain round.
        """
        self.view.display_success("Tour suivant...")
        self.generate_matches(new_tournament, new_tournament.list_rounds[round_index + 1])

    def end_tournament(self, new_tournament):
        """
        Termine le tournoi.
        """
        new_tournament.end_date = datetime.now()
        self.view.display_success("Fin du tournoi !")

    def gather_tournament_information(self):
        """
        Rassemble les informations pour créer un nouveau tournoi.
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
        Permet de choisir la méthode d'enregistrement des joueurs.
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
        Enregistre les joueurs automatiquement à partir d'un fichier et les ajoute au tournoi.
        """
        try:
            players = Player.read(self.file_player)
            new_tournament.players.extend(players)
            return new_tournament
        except Exception as e:
            raise Exception(f"Une erreur est survenue lors de l'enregistrement automatique des joueurs : {str(e)}")

    def register_players_manually(self, new_tournament):
        """
        Permet à l'utilisateur de sélectionner manuellement les joueurs à ajouter au tournoi.
        """
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

    def add_new_player(self, new_tournament):
        """
        Ajoute un nouveau joueur au tournoi.
        """
        while True:
            self.player_manager_controller = PlayerManagerController()
            new_player = self.player_manager_controller.create_player()
            new_tournament.players.append(new_player.as_dict())
            add_another = self.input_validator.validate_input(self.view.ask_add_another_player)
            if add_another == "o":
                continue
            else:
                return new_player
