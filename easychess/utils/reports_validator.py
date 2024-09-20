class ReportsInputValidator:
    def __init__(self, view):
        self.view = view

    def validate_menu_choice(self, choice):
        """
        Prompt and validate the user's choice.
        """
        if choice in ["0", "1", "2"]:
            return choice
        else:
            self.view.display_error("Veuillez saisir un choix entre 0, 1, 2 ou 3 !")
            return False
