############################################################################################################
#  REPORTS INPUT VALIDATOR                                                                                 #
############################################################################################################
class ReportsInputValidator:
    """
    Validates user input for generating reports in a chess tournament application.

    Attributes:
        utils (Utils): Utility methods for displaying messages and errors.
    """

    def __init__(self, utils):
        """
        Initializes the ReportsInputValidator.

        Args:
            utils (Utils): Utility methods for displaying messages.
        """
        self.utils = utils

    def validate_menu_choice(self, choice):
        """
        Validates the user's menu choice for report generation.

        Args:
            choice (str): The user's choice.

        Returns:
            str: The valid choice or False if invalid.
        """
        if choice in ["0", "1", "2", "3", "4"]:
            return choice
        else:
            self.utils.display_error("Veuillez saisir un choix entre 0, 1, 2, 3 ou 4 !")
            return False

    def validate_tournament_name(self, input_function, tournaments):
        """
        Validates the tournament name entered by the user.

        Args:
            input_function (callable): A function to get user input.
            tournaments (dict): A dictionary containing tournament data.

        Returns:
            str: The valid tournament name if found; keeps prompting until valid.
        """
        while True:
            tournament_name = input_function().strip()
            for tournament in tournaments.values():
                if tournament["name"] == tournament_name:
                    return tournament_name
            self.utils.display_error("Tournoi non trouvé. Veuillez réessayer.")
