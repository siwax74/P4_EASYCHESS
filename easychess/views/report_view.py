from easychess.utils.utils import Utils


class ReportView:
    def display_reports_menu(self) -> str:
        """
        Clears the terminal and displays the reports menu.

        This menu provides options for viewing players, tournaments, and details of a specific tournament.

        :return: The user's choice as a string.
        """
        Utils.clear_terminal()
        menu = "=" * 47 + "\n"
        menu += "         ♛ ♚ ♜ ♝ ♞ ♟ ♔ ♕ ♖ ♗ ♘ ♙ \n"
        menu += "                 EASYCHESS \n"
        menu += "=" * 47 + "\n"
        menu += "╔═════════════════════════════════════════════╗\n"
        menu += "║               MENU RAPPORTS                 ║\n"
        menu += "╚═════════════════════════════════════════════╝\n"
        menu += "╔═════════════════════════════════════════════╗\n"
        menu += "║  -- Actions --                              ║\n"
        menu += "║  1. Liste de tous les joueurs (A-Z)         ║\n"
        menu += "║  2. Liste de tous les tournois              ║\n"
        menu += "║  3. Détails d'un tournoi                    ║\n"
        menu += "║  0. Retour au menu principal                ║\n"
        menu += "╚═════════════════════════════════════════════╝\n"
        menu += "=" * 47 + "\n"
        print(menu)
        choice = input("Veuillez sélectionner une option : ")
        return choice

    def display_alphabetical_players(self, formatted_players):
        """
        Clears the terminal and displays a list of players in alphabetical order.

        This method formats and prints the list of players and waits for user input to return to the menu.

        :param formatted_players: A list of players formatted as strings.
        """
        Utils.clear_terminal()
        menu = "=" * 47 + "\n"
        menu += "         ♛ ♚ ♜ ♝ ♞ ♟ ♔ ♕ ♖ ♗ ♘ ♙ \n"
        menu += "                 EASYCHESS \n"
        menu += "=" * 47 + "\n"
        menu += "╔═════════════════════════════════════════════╗\n"
        menu += "║               MENU RAPPORTS                 ║\n"
        menu += "╚═════════════════════════════════════════════╝\n"
        menu += "=" * 47 + "\n"
        for player in formatted_players:
            menu += player + "\n"
        print(menu)

        choice = input("Veuillez saisir 0 + entrée pour revenir au menu : ")
        return choice

    def display_all_tournaments(self, tournaments):
        """
        Clears the terminal and displays a list of all tournaments.

        This method shows tournament details including name, start date, end date, number of rounds, and description.

        :param tournaments: A dictionary of tournaments with details.
        """
        Utils.clear_terminal()
        menu = "=" * 47 + "\n"
        menu += "         ♛ ♚ ♜ ♝ ♞ ♟ ♔ ♕ ♖ ♗ ♘ ♙ \n"
        menu += "                 EASYCHESS \n"
        menu += "=" * 47 + "\n"
        menu += "╔═════════════════════════════════════════════╗\n"
        menu += "║               MENU RAPPORTS                 ║\n"
        menu += "╚═════════════════════════════════════════════╝\n"
        menu += "=" * 47 + "\n"
        menu += "--- Liste des tournois ---"
        for key, tournament in tournaments.items():
            menu += f"\n{key}:\n"
            menu += f"  Nom: {tournament['name']}\n"
            menu += f"  Date de début: {tournament['start_date']}\n"
            menu += f"  Date de fin: {tournament['end_date']}\n"
            menu += f"  Localisation: {tournament['location']}\n"
            menu += f"  Nombre de tours: {tournament['number_of_rounds']}\n"
            menu += f"  Description: {tournament['description']}\n"
        print(menu)
        choice = input("Veuillez saisir 0 + entrée pour revenir au menu : ")
        return choice

    def display_tournaments_name(self, tournaments):
        """
        Clears the terminal and displays the names of all tournaments.

        This method formats and prints the names of the tournaments for user selection.

        :param tournaments: A dictionary of tournaments with their names.
        """
        Utils.clear_terminal()
        menu = "=" * 47 + "\n"
        menu += "         ♛ ♚ ♜ ♝ ♞ ♟ ♔ ♕ ♖ ♗ ♘ ♙ \n"
        menu += "                 EASYCHESS \n"
        menu += "=" * 47 + "\n"
        menu += "╔═════════════════════════════════════════════╗\n"
        menu += "║               MENU RAPPORTS                 ║\n"
        menu += "╚═════════════════════════════════════════════╝\n"
        menu += "=" * 47 + "\n"
        for key, tournament in tournaments.items():
            menu += f"{key}:\n"
            menu += f"  Nom: {tournament['name']}\n"
        print(menu)

    def ask_tournament_name_input(self):
        """
        Prompts the user for the name of a tournament.

        :return: The name of the tournament as a string.
        """
        tournament_name = input("Veuillez saisir le Nom du tournoi : ")
        return tournament_name

    def display_tournament_details(self, tournament, ranking_players):
        """
        Clears the terminal and displays the details of a specific tournament.

        This includes the tournament's name, location, dates, player list, match details, and rankings.

        :param tournament: A dictionary containing details of the tournament.
        :param ranking_players: A list of players with their ranking and scores.
        """
        Utils.clear_terminal()
        menu = "=" * 47 + "\n"
        menu += "         ♛ ♚ ♜ ♝ ♞ ♟ ♔ ♕ ♖ ♗ ♘ ♙ \n"
        menu += "                 EASYCHESS \n"
        menu += "=" * 47 + "\n"
        menu += "╔═════════════════════════════════════════════╗\n"
        menu += "║               DÉTAILS DU TOURNOI            ║\n"
        menu += "╚═════════════════════════════════════════════╝\n"
        menu += "=" * 47 + "\n"
        menu += f"Nom: {tournament['name']}\n"
        menu += f"Lieu: {tournament['location']}\n"
        menu += f"Date de début: {tournament['start_date']}\n"
        menu += f"Date de fin: {tournament['end_date']}\n"
        menu += "  Liste des joueurs:\n"
        for player in tournament["players"]:
            menu += f"    - {player['last_name']} {player['first_name']}\n"
        menu += "  Liste des tours:\n"
        for round in tournament["list_rounds"]:
            menu += f"    - {round['name']}\n"
            menu += "      Matchs:\n"
            for match in round["matches"]:
                menu += f"        - {match[0][0]} vs {match[1][0]} - Score: {match[0][1]}-{match[1][1]}\n"
        menu += "  Classement des joueurs:\n"
        for player in ranking_players:
            menu += f"    - {player['last_name']} {player['first_name']} -  Score: {player['score']}\n"

        menu += f"  Description: {tournament['description']}\n"
        print(menu)
        choice = input("Veuillez saisir 0 + entrée pour revenir au menu : ")
        return choice
