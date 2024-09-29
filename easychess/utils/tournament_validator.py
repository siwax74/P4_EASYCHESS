############################################################################################################
#  TOURNAMENT INPUT VALIDATOR                                                                              #
############################################################################################################
import re


class TournamentInputValidator:
    def __init__(self, utils, file_player, sanitize):
        """
        Initialize the TournamentInputValidator.

        :param utils: Utility functions for displaying messages and errors.
        :param file_player: Path to the player file.
        :param sanitize: An instance of the Sanitize class for text sanitization.
        """
        self.utils = utils
        self.file_player = file_player
        self.sanitize = sanitize

    ############################################################################################################
    #                                                VALID MENU CHOICE                                         #
    ############################################################################################################
    def validate_menu_choice(self, choice):
        """
        Prompt and validate the user's menu choice.

        :param choice: The user's choice input.
        :return: The validated choice or False if invalid.
        """
        if choice in ["0", "1", "2"]:
            return choice
        else:
            self.utils.display_error("Veuillez saisir un choix entre 0, 1, 2 ! ")
            return False

    ############################################################################################################
    #                                                VALID NAME                                                #
    ############################################################################################################
    def validate_name(self, input_function):
        """
        Validate the tournament name input.

        :param input_function: Function to get user input.
        :return: The sanitized name or False if invalid.
        """
        pattern = "^[0A-Za-zÀ-ÖØ-öø-ÿ' -]+$"
        while True:
            name = input_function().strip()
            if not (1 <= len(name) <= 50):
                self.utils.display_error("Veuillez saisir un nom valide !")
            elif not re.match(pattern, name):
                self.utils.display_error("Le nom ne peut pas contenir de caractères spéciaux !")
            elif name == "0":
                return False
            else:
                return self.sanitize.sanitize_text(name)

    ############################################################################################################
    #                                                VALID LOCATION                                            #
    ############################################################################################################
    def validate_location(self, input_function):
        """
        Validate the tournament location input.

        :param input_function: Function to get user input.
        :return: The sanitized location or False if invalid.
        """
        pattern = "^[,0-9A-Za-zÀ-ÖØ-öø-ÿ' -]+$"
        while True:
            location = input_function().strip()
            if not (1 <= len(location) <= 50):
                self.utils.display_error("Veuillez saisir un lieu valide !")
            elif not re.match(pattern, location):
                self.utils.display_error("Le lieu ne peut pas contenir de caractères spéciaux !")
            elif location == "0":
                return False
            else:
                return self.sanitize.sanitize_text(location)

    ############################################################################################################
    #                                               VALID DESCRIPTION                                          #
    ############################################################################################################
    def validate_description(self, input_function):
        """
        Validate the tournament description input.

        :param input_function: Function to get user input.
        :return: The sanitized description or False if invalid.
        """
        while True:
            description = input_function().strip()
            if not (5 <= len(description) <= 200):
                self.utils.display_error("La description doit être entre 5 et 200 caractères !")
            elif description == "0":
                return False
            else:
                return self.sanitize.sanitize_text(description)

    ############################################################################################################
    #                                           VALID REGISTRATION METHOD                                      #
    ############################################################################################################
    def validate_registration_method(self, choice):
        """
        Validate the tournament registration method.

        :param choice: The user's choice for registration method.
        :return: The validated choice or False if invalid.
        """
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
        Validate the selection of players for the tournament.

        :param input_function: Function to get user input.
        :param players: List of players available for selection.
        :return: The validated player selection.
        """
        while True:
            selected_players = input_function(players).strip()
            if self.is_valid_player_selection(selected_players, players):
                return selected_players

    def is_valid_player_selection(self, selected_players, players):
        """
        Check if the selected players are valid.

        :param selected_players: The string of selected player indices.
        :param players: List of players available for selection.
        :return: True if valid, False otherwise.
        """
        try:
            selected_players = [int(i) - 1 for i in selected_players.split()]
            if any(idx < 0 or idx >= len(players) for idx in selected_players):
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
        Validate user input for yes/no responses.

        :param input_function: Function to get user input.
        :return: The validated response.
        """
        while True:
            response = input_function().strip()
            if response in ["o", "n", "0"]:
                return response
            else:
                self.utils.display_error("Veuillez répondre par o, n ou 0 !")

    def validate_add_new_player(self, input_function):
        """
        Validate user input for yes/no responses.

        :param input_function: Function to get user input.
        :return: The validated response.
        """
        while True:
            response = input_function().strip()
            if response in ["o", "n", "0"]:
                return response
            else:
                self.utils.display_error("Veuillez répondre par o, n ou 0 !")

    ############################################################################################################
    #                                                VALID RETURN TO MENU                                      #
    ############################################################################################################
    def validate_return_to_menu(self, input_function):
        """
        Validate user input for returning to the menu.

        :param input_function: Function to get user input.
        :return: The response to return to the menu.
        """
        while True:
            response = input_function().strip()
            if response == "0":
                return response
            else:
                self.utils.display_error("Saisir 0 pour revenir au menu !")
                return False

    ############################################################################################################
    #                                                VALID MATCH INPUT                                         #
    ############################################################################################################
    def validate_match(self, input_winner):
        """
        Validate user input for determining the winner of a match.

        :param input_winner: User input for the match winner.
        :return: The validated input for the winner.
        """
        while True:
            if input_winner in ["0", "1", "2"]:
                return input_winner
            else:
                self.utils.display_error("Erreur de saisi ! Gagnant : Joueur1 (1) ou Joueur2 (2) ou match nul (0)")
                return False

    ############################################################################################################
    #                                                VALID TOURNAMENT INDEX INPUT                              #
    ############################################################################################################
    def validate_tournament_index(self, input_function, none_status_tournaments):
        while True:
            try:
                tournament_index = int(input_function())
                if tournament_index in none_status_tournaments:
                    return tournament_index
                else:
                    print("Erreur : Index invalide. Veuillez saisir un index valide.")
            except ValueError:
                print("Erreur : Veuillez saisir un nombre entier.")
