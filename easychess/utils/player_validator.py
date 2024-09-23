############################################################################################################
#  PLAYER VALIDATOR                                                                                        #
############################################################################################################
from datetime import datetime
import re


class PlayerInputValidator:
    def __init__(self, utils, sanitize):
        """
        Initializes the PlayerInputValidator with utility and sanitization classes.

        :param utils: Utility functions for displaying messages.
        :param sanitize: Object for sanitizing input data.
        """
        self.utils = utils
        self.sanitize = sanitize

    ############################################################################################################
    #                                                VALID INPUT                                               #
    ############################################################################################################
    def validate_return_to_menu(self, input_function):
        """
        Validates the user's response for returning to the menu.

        :param input_function: Function to get user input.
        :return: "0" if the user wants to return to the menu, False otherwise.
        """
        while True:
            response = input_function().strip()
            if response == "0":
                return response
            else:
                self.utils.display_error("Saisir 0 pour revenir au menu !")
                return False

    ############################################################################################################
    #                                                VALID CHOICE MENU                                         #
    ############################################################################################################
    def validate_choice(self, choice):
        """
        Validates the user's menu choice.

        :param choice: User's choice input.
        :return: Validated choice or False if invalid.
        """
        if choice in ["0", "1", "2", "3"]:
            return choice
        else:
            self.utils.display_error("Veuillez saisir un choix entre 0, 1, 2 ou 3 !")
            return False

    ############################################################################################################
    #                                                INFO_NAME/SURNAME                                         #
    ############################################################################################################
    def validate_info(self, input_function):
        """
        Validates a name or surname input from the user.

        :param input_function: Function to get user input.
        :return: Sanitized name or surname if valid, or False if input is "0".
        """
        while True:
            info = input_function().strip()
            if re.match("^[A-Za-zÀ-ÖØ-öø-ÿ' -]+$", info):
                sanitize_info = self.sanitize.sanitize_text(info)
                return sanitize_info
            elif info == "0":
                return False
            elif not re.match("^[A-Za-zÀ-ÖØ-öø-ÿ' -]+$", info):
                self.utils.display_error("Le Prénom/Nom ne peut pas contenir de caractères spéciaux !")

    ############################################################################################################
    #                                                BIRTHDATE                                                 #
    ############################################################################################################
    def validate_birthdate(self, input_function):
        """
        Validates a birthdate input from the user.

        :param input_function: Function to get user input.
        :return: Validated birthdate in "dd/mm/YYYY" format, or False if input is "0".
        """
        while True:
            birthdate = input_function()
            try:
                datetime.strptime(birthdate, "%d/%m/%Y")
                return birthdate
            except ValueError:
                if birthdate == "0":
                    return False
                else:
                    self.utils.display_error("Veuillez saisir une date au format 'dd/mm/YYYY' !")

    ############################################################################################################
    #                                                NATIONAL_ID                                               #
    ############################################################################################################
    def validate_national_id(self, input_function):
        """
        Validates a national ID input from the user.

        :param input_function: Function to get user input.
        :return: Validated national ID or False if input is "0".
        """
        while True:
            national_id = input_function()
            if national_id == "0":
                return False
            if not national_id:
                return national_id
            elif len(national_id) > 7 or not re.match("^[A-Za-z0-9]{2}[0-9]{5}$", national_id):
                self.utils.display_error("Veuillez saisir un national_id valide au format 'AB12345' !")
            else:
                return national_id
