class ReportsInputValidator:
    def __init__(self, view):
        self.view = view

    def validate_menu_choice(self, choice):
        """
        Prompt and validate the user's choice.
        """
        if choice in ["0", "1", "2", "3", "4"]:
            return choice
        else:
            self.view.display_error("Veuillez saisir un choix entre 0, 1, 2 ou 3 !")
            return False

    def validate_tournament_name(self, input_function, tournaments):
        while True:
            tournament_name = input_function().strip()
            for tournament in tournaments.values():
                if tournament["name"] == tournament_name:
                    return tournament_name
            else:
                self.view.display_error("Tournoi non trouvé")
                continue