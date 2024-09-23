from datetime import datetime
import random
from easychess.utils.utils import Utils
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
        self.utils = Utils()
        self.sanitize = Sanitize(self.view)
        self.input_validator = TournamentInputValidator(self.utils, self.file_player, self.sanitize)

    def show_menu_options(self):
        """
        Displays the main menu options and handles user choices.

        This method presents a menu to the user, allowing them to select
        different options related to tournaments. It continuously prompts
        for input until the user chooses to exit.

        The user can make the following choices:
        - '1': Create and start a new tournament.
        - '0': Exit the menu.

        If the user selects '1', a new tournament is created and started.
        If the user selects '0', the loop breaks and the method ends.
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
        Creates a new tournament based on the user's choice.

        Parameters:
        - choice (str): The user's selection from the menu, which determines the tournament type.

        Returns:
        - Tournament|bool: Returns the newly created tournament object if successful,
                         or False if the creation fails at any point.

        Process:
        1. Checks if the choice is valid. If not, returns False.
        2. Gathers necessary tournament information from the user.
        3. If gathering information fails, returns False.
        4. Creates a new tournament using the gathered information.
        5. Allows the user to choose a method for player registration.
        6. If player registration method selection fails, returns False.
        7. Generates the tournament.
        8. If tournament generation fails, returns False.
        9. Displays a success message upon successful tournament creation.
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
        self.utils.display_success("Tournament generation successful!")
        return new_tournament

    def generate_tournament(self, new_tournament):
        """
        Manages the initiation of the tournament.

        Parameters:
        - new_tournament (Tournament): The tournament object to be initiated.

        Returns:
        - Tournament: The new tournament object if it starts successfully.
        - str: '0' if the user chooses to exit.
        - None: If the input is invalid (neither confirmation nor exit).

        Process:
        1. Prompts the user for input to start the tournament.
        2. If the user confirms with 'o', generates the rounds for the tournament.
        3. Generates matches for the first round of the tournament.
        4. Returns the tournament object if successfully initiated.
        5. If the user chooses to exit, returns '0'.
        6. If the input is neither confirmation nor exit, returns None.
        """
        choice = self.input_validator.validate_input(self.view.ask_start_tournament)
        if choice == "o":
            list_rounds = self.generate_rounds(new_tournament)
            self.generate_matches(new_tournament, list_rounds[0])
            return new_tournament
        return choice if choice == "0" else None

    def generate_rounds(self, new_tournament):
        """
        Generates the necessary rounds for the tournament.

        Parameters:
        - new_tournament (Tournament): The tournament object for which the rounds are being generated.

        Returns:
        - list: A list of created Round objects representing the rounds for the tournament.

        Process:
        1. Determines the number of players in the tournament.
        2. Calculates the number of rounds (usually one less than the number of players).
        3. Iterates through the calculated number of rounds.
        4. For each round, creates a new `Round` object and adds it to both the internal list of rounds
        and the tournament's `list_rounds`.
        5. Returns the list of all generated rounds.
        """
        num_players = len(new_tournament.players)
        num_rounds = num_players - 1
        list_rounds = []
        for i in range(1, num_rounds + 1):
            round_name = f"Round {i}"
            round_obj = Round.create(round_name)
            list_rounds.append(round_obj)
            new_tournament.list_rounds.append(round_obj)
        return list_rounds

    def get_players(self, new_tournament):
        """
        Retrieves the list of players from the tournament.

        Parameters:
        - new_tournament (Tournament): The tournament object from which to retrieve the players.

        Returns:
        - list: A list of player objects in the tournament.

        Raises:
        - ValueError: If there are fewer than 2 players, since a minimum of 2 is required to create matches.

        Process:
        1. Retrieves the list of players from the `new_tournament` object.
        2. Checks if the number of players is less than 2.
        3. If fewer than 2 players are found, raises a `ValueError` indicating that there are not enough players.
        4. If valid, returns the list of players.
        """
        players = new_tournament.players
        if len(players) < 2:
            raise ValueError("Not enough players to create matches.")
        return players

    def shuffle_players(self, players):
        """
        Shuffles the list of players randomly.

        Parameters:
        - players (list): A list of player objects to be shuffled.

        Returns:
        - list: The shuffled list of players.

        Process:
        1. Uses the `random.shuffle()` function to randomize the order of players in place.
        2. Returns the shuffled list of players.
        """
        random.shuffle(players)
        return players

    def sort_players_by_score(self, players_shuffle):
        """
        Sorts the list of players based on their score in descending order.

        Parameters:
        - players_shuffle (list): A list of player objects that have a "score" attribute.

        Returns:
        - list: A list of players sorted by their score, from highest to lowest.

        Process:
        1. Uses the `sorted()` function to sort the players based on the "score" attribute.
        2. Sorting is done in descending order (highest score first).
        3. Returns the sorted list of players.
        """
        players_sorted = sorted(players_shuffle, key=lambda x: x["score"], reverse=True)
        return players_sorted

    def generate_matches(self, new_tournament, round):
        """
        Generates player pairings for a given round in the tournament.

        Parameters:
        - new_tournament (Tournament): The tournament object for which the matches are being generated.
        - round (Round): The specific round object in which the matches will take place.

        Process:
        1. Retrieves the list of players from the tournament using `get_players()`.
        2. Randomly shuffles the players using `shuffle_players()`.
        3. Sorts the shuffled players by their score using `sort_players_by_score()`,
        to ensure that pairings are based on ranking.
        4. Calls `create_matches()` to generate and assign the matches for the sorted players within the round.
        """
        players = self.get_players(new_tournament)
        players_shuffle = self.shuffle_players(players)
        players_sorted = self.sort_players_by_score(players_shuffle)
        self.create_matches(players_sorted, round, new_tournament)

    def create_matches(self, players_sorted, round, tournament):
        """
        Creates matches for a given round, ensuring that players don't play against the same opponent multiple times.

        Parameters:
        - players_sorted (list): A list of player objects, sorted by their score.
        - round (Round): The round object where the matches will be added.
        - tournament (Tournament): The tournament object that tracks previous matches between players.

        Process:
        1. Initializes an empty list for the round's matches and a set to track matched players.
        2. Iterates over the sorted players and attempts to pair each player with another that they haven't met.
        3. Uses `have_players_met()` to check if two players have already played against each other.
        4. If a valid opponent is found, a match is created and added to the round.
        5. If no new opponent can be found, the player is matched with the next available player.
        6. Handles the case of an odd number of players by calling `handle_odd_player()` for the last unmatched player.
        """
        round.matches = []
        matched_players = set()

        for i in range(0, len(players_sorted)):
            if i + 1 >= len(players_sorted):
                break

            player1 = players_sorted[i]

            # Find an opponent that player1 hasn't met yet
            for j in range(i + 1, len(players_sorted)):
                player2 = players_sorted[j]
                if not self.have_players_met(player1, player2, tournament):
                    match = Match.create(player1, player2)
                    round.add_match(match)
                    matched_players.add(player1["last_name"])
                    matched_players.add(player2["last_name"])
                    players_sorted.pop(j)  # Remove player2 after match is created
                    break

            # If player1 hasn't been matched, pair with next available player
            if player1["last_name"] not in matched_players:
                player2 = players_sorted[i + 1]
                match = Match.create(player1, player2)
                round.add_match(match)
                matched_players.add(player1["last_name"])
                matched_players.add(player2["last_name"])

        # Handle case of odd number of players
        if len(players_sorted) % 2 != 0:
            last_player = players_sorted[-1]
            if last_player["last_name"] not in matched_players:
                self.handle_odd_player(last_player, round)

    def have_players_met(self, player1, player2, tournament):
        """
        Checks if two players have already played against each other in the tournament.

        Parameters:
        - player1 (dict): The first player's data, containing at least the "last_name" key.
        - player2 (dict): The second player's data, containing at least the "last_name" key.
        - tournament (Tournament): The tournament object that contains the list of rounds and matches played.

        Returns:
        - bool: Returns True if the two players have already met in the tournament, False otherwise.

        Process:
        1. Iterates through each round in the tournament.
        2. For each round, checks all matches to see if `player1` and `player2` have faced each other.
        3. A match is considered a meeting if:
        - `player1`'s last name matches `player2`'s opponent's last name and vice versa.
        4. Returns `True` if a match between them is found, otherwise `False`.
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

    def handle_odd_player(self, player, round):
        """
        Gère le cas d'un nombre impair de joueurs.
        """
        pass

    def start_tournament(self, new_tournament):
        """
        Manages the flow of the tournament, executing each round and handling transitions between rounds.

        Parameters:
        - new_tournament (Tournament): The tournament object to be managed,
                                       which contains all the necessary tournament data.

        Returns:
        - bool: Returns False if the tournament is invalid or cannot start,
                otherwise proceeds with the tournament flow.

        Process:
        1. If `new_tournament` is invalid, returns `False`.
        2. Sets the tournament's start date to the current date and time.
        3. Iterates over the total number of rounds in the tournament:
        - For each round, calls `play_round()` to execute the matches.
        - If it is not the last round, prepares the next round using `prepare_next_round()`.
        - Displays each player's opponents after each round.
        4. After the last round, calls `end_tournament()` to conclude the tournament.
        5. Saves the tournament's state (as a dictionary) to a file for persistence using `Tournament.save()`.
        """
        if not new_tournament:
            return False
        new_tournament.start_date = datetime.now()
        num_rounds = new_tournament.number_of_rounds
        for round_index in range(new_tournament.number_of_rounds):
            round = new_tournament.list_rounds[round_index]
            self.play_round(round, round_index, num_rounds)
            if round_index < new_tournament.number_of_rounds - 1:
                self.prepare_next_round(new_tournament, round_index)
                for player in new_tournament.players:
                    print(f"Player {player['last_name']}: Opponents = {player.get('opponents', set())}")
            else:
                self.end_tournament(new_tournament)

    def play_round(self, round, round_index, num_rounds):
        """
        Plays a round of the tournament by processing each match in the round.

        Parameters:
        - round (Round): The round object that contains the matches to be played.
        - round_index (int): The current round number (index) being played.
        - num_rounds (int): The total number of rounds in the tournament.

        Process:
        1. Iterates over each match in the round.
        2. For each match, displays the round details using 'self.view.display()',
             which shows the current round and match information.
        3. Calls `play_match()` for each match, passing the match object and its index within the round.
        4. Sets the round's `end_date_time` to the current date and time once all matches in the round have been played
        """
        for match_index, match in enumerate(round.matches):
            self.view.display(round, round_index, num_rounds)
            self.play_match(match, match_index)
        round.end_date_time = datetime.now()

    def play_match(self, match, match_index):
        """
        Plays a match between two players, updates scores, and tracks opponents.

        Parameters:
        - match (Match): The match object containing the players and their scores.
        - match_index (int): The index of the match in the round.

        Process:
        1. Prompts for the winner of the match using `self.view.ask_validate_match()`, which returns the user's input.
        2. Validates the input with `self.input_validator.validate_match()`.
        3. Depending on the user input:
        - If "1", player 1 wins, score is set to (1, 0), and player 1's score is updated.
        - If "2", player 2 wins, score is set to (0, 1), and player 2's score is updated.
        - If "0", it's a draw, score is set to (0.5, 0.5), and both players' scores are updated.
        4. Updates each player's opponents list with the other player's last name.
        5. Prints the current opponents of both players for reference.
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

        match.player1.setdefault("opponents", set()).add(match.player2["last_name"])
        match.player2.setdefault("opponents", set()).add(match.player1["last_name"])

        print(f"Player 1 ({match.player1['last_name']}): Opponents = {match.player1.get('opponents', set())}")
        print(f"Player 2 ({match.player2['last_name']}): Opponents = {match.player2.get('opponents', set())}")

    def prepare_next_round(self, new_tournament, round_index):
        """
        Prepares the next round of the tournament by generating matches.

        Parameters:
        - new_tournament (Tournament): The tournament object containing the rounds and players.
        - round_index (int): The index of the current round, used to identify the next round.

        Process:
        1. Displays a success message indicating that the next round is starting.
        2. Calls generate_matches() to create matches for the next round, using the round object at round_index + 1.
        """
        self.utils.display_success("Tour suivant...")
        self.generate_matches(new_tournament, new_tournament.list_rounds[round_index + 1])

    def end_tournament(self, new_tournament):
        """
        Ends the tournament and performs final cleanup.

        Parameters:
        - new_tournament (Tournament): The tournament object that needs to be concluded.

        Process:
        1. Sets the tournament's end date to the current date and time.
        2. Iterates through each player in the tournament:
        - Removes the "opponents" attribute from each player, cleaning up the player data.
        3. Displays a success message indicating that the tournament has ended.
        4. Saves the final state of the tournament to a file for persistence using `Tournament.save()`.
        """
        new_tournament.end_date = datetime.now()
        for player in new_tournament.players:
            if "opponents" in player:
                del player["opponents"]
        self.utils.display_success("Fin du tournoi !")
        Tournament.save(self.file_tournament, new_tournament.as_dict())

    def gather_tournament_information(self):
        """
        Gathers information required to create a new tournament.

        Returns:
        - tuple: A tuple containing the tournament's name, location, and description if valid input is provided.
        - bool: Returns False if any input validation fails.

        Process:
        1. Continuously prompts the user for the tournament's name, location, and description.
        2. Each input is validated using the respective validation methods.
        3. If any input is invalid (returns False), the process is halted, and False is returned.
        4. If all inputs are valid, returns a tuple containing (name, location, description).
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
        Allows the user to choose the method for registering players in the tournament.

        Parameters:
        - new_tournament (Tournament): The tournament object where players will be registered.

        Returns:
        - Depending on the chosen method:
            - bool: True if players were registered automatically.
            - list: A list of players added if registered manually.
            - dict: A dictionary of the new player added if a new player is registered.
            - None: If the user chooses to exit the registration process.

        Process:
        1. Continuously prompts the user to select a registration method for players.
        2. Validates the user's choice using `self.input_validator.validate_registration_method()`.
        3. Based on the user's choice:
        - If "0", exits the registration process.
        - If "1", calls `register_players_automatically()` to register players automatically.
        - If "2", calls `register_players_manually()` to allow for manual registration of players.
        - If "3", calls `add_new_player()` to add a single new player to the tournament.
        4. Returns the result of the selected registration method.
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

        Parameters:
        - new_tournament (Tournament): The tournament object to which players will be added.

        Returns:
        - Tournament: The updated tournament object with the newly registered players.

        Process:
        1. Attempts to read player data from a specified file using `Player.read()`.
        2. Extends the tournament's player list with the players retrieved from the file.
        3. Returns the updated tournament object.

        Raises:
        - Exception: If an error occurs during the reading of the player file or adding players to the tournament.
        """
        try:
            players = Player.read(self.file_player)
            new_tournament.players.extend(players)
            return new_tournament
        except Exception as e:
            raise Exception(f"Une erreur est survenue lors de l'enregistrement automatique des joueurs : {str(e)}")

    def register_players_manually(self, new_tournament):
        """
        Allows the user to manually select players to add to the tournament.

        Parameters:
        - new_tournament (Tournament): The tournament object to which players will be added.

        Returns:
        - Tournament: The updated tournament object with the newly registered players.

        Process:
        1. Reads the list of available players from a specified file using `Player.read()`.
        2. Prompts the user to select players using `self.view.ask_player_selection`.
        3. Validates the selected player indices with `self.input_validator.validate_selected_players()`.
        4. Converts the selected player indices from string to integer and adjusts for zero-based indexing.
        5. For each selected index, checks if it is valid:
        - If valid, the corresponding player is appended to the tournament's player list.
        - If invalid, raises an `IndexError` with a relevant message.
        6. Returns the updated tournament object.

        Raises:
        - Exception: If any error occurs.
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
        Adds a new player to the tournament.

        Parameters:
        - new_tournament (Tournament): The tournament object to which the new player will be added.

        Returns:
        - dict: The newly added player as a dictionary if the user decides to stop adding players.

        Process:
        1. Initializes a `PlayerManagerController` instance to manage player creation.
        2. Continuously prompts the user to create a new player using `create_player()`.
        3. Appends the newly created player's data (as a dictionary) to the tournament's player list.
        4. Asks the user if they want to add another player using `self.view.ask_add_another_player`.
        5. If the user responds with "yes" (or equivalent), the process repeats.
        6. If the user responds with "no", returns the newly added player.
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
