############################################################################################################
#  REPORTS VALIDATOR                                                                                       #
############################################################################################################
class ReportsInputValidator:
    def __init__(self, utils):
        """
        Initializes the ReportsInputValidator with utility functions.

        :param utils: Utility functions for displaying messages.
        """
        self.utils = utils

    def validate_menu_choice(self, choice):
        """
        Validates the user's menu choice.

        :param choice: User's choice input.
        :return: Validated choice if valid, or False if invalid.
        """
        if choice in ["0", "1", "2", "3", "4"]:
            return choice
        else:
            self.utils.display_error("Veuillez saisir un choix entre 0, 1, 2 ou 3 !")
            return False

    def validate_tournament_name(self, input_function, tournaments):
        """
        Validates the tournament name provided by the user.

        :param input_function: Function to get user input.
        :param tournaments: Dictionary of existing tournaments.
        :return: Validated tournament name if found, or prompts for a valid name until one is provided.
        """
        while True:
            tournament_name = input_function().strip()
            for tournament in tournaments.values():
                if tournament["name"] == tournament_name:
                    return tournament_name
            else:
                self.utils.display_error("Tournoi non trouvé")
                continue
