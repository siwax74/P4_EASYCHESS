############################################################################################################
#  TOURNAMENT VALIDATOR                                                                                     #
############################################################################################################
import re


class TournamentInputValidator:
    def __init__(self, utils, file_player, sanitize):
        """
        Initializes the TournamentInputValidator with utility functions, player file, and sanitization tools.

        :param utils: Utility functions for displaying messages and errors.
        :param file_player: Path to the player file.
        :param sanitize: Sanitization tool for input text.
        """
        self.utils = utils
        self.file_player = file_player
        self.sanitize = sanitize

    ############################################################################################################
    #                                                VALID MENU CHOICE                                         #
    ############################################################################################################
    def validate_menu_choice(self, choice):
        """
        Validates the user's menu choice.

        :param choice: User's input choice.
        :return: Validated choice or False if invalid.
        """
        if choice in ["0", "1", "2", "3", "4", "5"]:
            return choice
        else:
            self.utils.display_error("Veuillez saisir un choix entre 0, 1, 2, 3, 4 ou 5 !")
            return False

    ############################################################################################################
    #                                                VALID NAME                                                #
    ############################################################################################################
    def validate_name(self, input_function):
        """
        Validates the tournament name input.

        :param input_function: Function to get user input.
        :return: Sanitized tournament name or False if invalid.
        """
        pattern = "^[0A-Za-zÀ-ÖØ-öø-ÿ' -]+$"
        while True:
            name = input_function().strip()
            if len(name) < 1 or len(name) > 50:
                self.utils.display_error("Veuillez saisir un nom valide !")
            elif not re.match(pattern, name):
                self.utils.display_error("Le nom ne peut pas contenir de caractères spéciaux !")
            elif name == "0":
                return False
            else:
                name_sanitized = self.sanitize.sanitize_text(name)
                return name_sanitized

    ############################################################################################################
    #                                                VALID LOCATION                                            #
    ############################################################################################################
    def validate_location(self, input_function):
        """
        Validates the tournament location input.

        :param input_function: Function to get user input.
        :return: Sanitized location or False if invalid.
        """
        pattern = "^[,0-9A-Za-zÀ-ÖØ-öø-ÿ' -]+$"
        while True:
            location = input_function().strip()
            if len(location) < 1 or len(location) > 50:
                self.utils.display_error("Veuillez saisir un lieu valide !")
            elif not re.match(pattern, location):
                self.utils.display_error("Le lieu ne peut pas contenir de caractères spéciaux !")
            elif location == "0":
                return False
            else:
                location_sanitized = self.sanitize.sanitize_text(location)
                return location_sanitized

    ############################################################################################################
    #                                               VALID DESCRIPTION                                          #
    ############################################################################################################
    def validate_description(self, input_function):
        """
        Validates the tournament description input.

        :param input_function: Function to get user input.
        :return: Sanitized description or False if invalid.
        """
        while True:
            description = input_function().strip()
            if len(description) < 5 or len(description) > 200:
                self.utils.display_error("La description doit être entre 5 et 200 caractères !")
            elif description == "0":
                return False
            else:
                description_sanitized = self.sanitize.sanitize_text(description)
                return description_sanitized

    ############################################################################################################
    #                                           VALID REGISTRATION METHOD                                      #
    ############################################################################################################
    def validate_registration_method(self, choice):
        """
        Validates the user's choice for the player registration method.

        :param choice: User's input choice.
        :return: Validated choice or False if invalid.
        """
        while True:
            if choice in ["1", "2", "3", "0"]:
                return choice
            else:
                self.utils.display_error("Veuillez choisir une option valide : 1, 2, 3 ou 0.")
                return False

    ############################################################################################################
    #                                             VALID PLAYER SELECTION                                       #
    ############################################################################################################
    def validate_selected_players(self, input_function, players):
        """
        Validates the user's selection of players.

        :param input_function: Function to get user input.
        :param players: List of players to validate against.
        :return: Validated player selections.
        """
        while True:
            selected_players = input_function(players).strip()
            if self.is_valid_player_selection(selected_players, players):
                return selected_players

    def is_valid_player_selection(self, selected_players, players):
        """
        Checks if the selected player indices are valid.

        :param selected_players: User's selected player indices.
        :param players: List of available players.
        :return: True if valid, otherwise False.
        """
        try:
            selected_players = [int(i) - 1 for i in selected_players.split()]
            for idx in selected_players:
                if idx < 0 or idx >= len(players):
                    self.utils.display_error("Le joueur à cet index n'existe pas.")
                    return False
            return True
        except ValueError:
            self.utils.display_error("Veuillez saisir des indices de joueurs valides.")
            return False

    ############################################################################################################
    #                                             VALID INPUT   o/n                                            #
    ############################################################################################################
    def validate_input(self, input_function):
        """
        Validates a yes/no input from the user.

        :param input_function: Function to get user input.
        :return: Validated response (o, n, or 0).
        """
        while True:
            response = input_function().strip()
            if response in ["o", "n", "0"]:
                return response
            else:
                self.utils.display_error("Veuillez répondre par o, n ou 0 ! ")

    ############################################################################################################
    #                                                VALID INPUT                                               #
    ############################################################################################################
    def validate_return_to_menu(self, input_function):
        """
        Validates the input to return to the menu.

        :param input_function: Function to get user input.
        :return: Validated response (0 to return).
        """
        while True:
            response = input_function().strip()
            if response == "0":
                return response
            else:
                self.utils.display_error("Saisir 0 pour revenir au menu !")
                return False

    ############################################################################################################
    #                                                VALID INPUT                                               #
    ############################################################################################################
    def validate_match(self, input_winner):
        """
        Validates the user's input to determine the winner of a match.

        :param input_winner: User's input indicating the winner.
        :return: Validated winner input (0, 1, or 2).
        """
        if input_winner in ["0", "1", "2"]:
            return input_winner
        else:
            self.utils.display_error("Erreur de saisi ! Gagnant : Joueur1 (1) ou Joueur2 (2) ou match nul (0)")
