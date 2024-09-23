from easychess.utils.utils import Utils


class TournamentView:
    def display_tournament_menu(self) -> str:
        """
        Clears the terminal and displays the tournament menu.

        This menu provides options for managing tournaments.

        :return: The user's choice as a string.
        """
        Utils.clear_terminal()
        menu = "=" * 47 + "\n"
        menu += "         ♛ ♚ ♜ ♝ ♞ ♟ ♔ ♕ ♖ ♗ ♘ ♙ \n"
        menu += "                 EASYCHESS \n"
        menu += "=" * 47 + "\n"
        menu += "╔═════════════════════════════════════════════╗\n"
        menu += "║               MENU TOURNOIS                 ║\n"
        menu += "╚═════════════════════════════════════════════╝\n"
        menu += "╔═════════════════════════════════════════════╗\n"
        menu += "║  -- Actions --                              ║\n"
        menu += "║  0. Revenir au menu principal               ║\n"
        menu += "║  1. Ajouter/démarrer nouveau tournoi        ║\n"
        menu += "╚═════════════════════════════════════════════╝\n"
        menu += "=" * 47 + "\n"
        print(menu)
        choice = input("Entrez votre choix : ")
        return choice

    def ask_name(self):
        """
        Prompts the user for the name of the tournament.

        :return: The name of the tournament as a string.
        """
        Utils.clear_terminal()
        menu = "=" * 47 + "\n"
        menu += "         ♛ ♚ ♜ ♝ ♞ ♟ ♔ ♕ ♖ ♗ ♘ ♙ \n"
        menu += "                 EASYCHESS \n"
        menu += "=" * 47 + "\n"
        menu += "╔═════════════════════════════════════════════╗\n"
        menu += "║               MENU TOURNOIS                 ║\n"
        menu += "╚═════════════════════════════════════════════╝\n"
        menu += "0. Revenir au menu tournois\n"
        print(menu)
        name = input("Entrez le nom du tournoi : ")
        return name

    def ask_location(self):
        """
        Prompts the user for the location of the tournament.

        :return: The location of the tournament as a string.
        """
        Utils.clear_terminal()
        menu = "=" * 47 + "\n"
        menu += "         ♛ ♚ ♜ ♝ ♞ ♟ ♔ ♕ ♖ ♗ ♘ ♙ \n"
        menu += "                 EASYCHESS \n"
        menu += "=" * 47 + "\n"
        menu += "╔═════════════════════════════════════════════╗\n"
        menu += "║               MENU TOURNOIS                 ║\n"
        menu += "╚═════════════════════════════════════════════╝\n"
        menu += "0. Revenir au menu principal\n"
        print(menu)
        location = input("Entrez la localisation du tournoi : ")
        return location

    def ask_description(self):
        """
        Prompts the user for a description of the tournament.

        :return: The description of the tournament as a string.
        """
        Utils.clear_terminal()
        menu = "=" * 47 + "\n"
        menu += "         ♛ ♚ ♜ ♝ ♞ ♟ ♔ ♕ ♖ ♗ ♘ ♙ \n"
        menu += "                 EASYCHESS \n"
        menu += "=" * 47 + "\n"
        menu += "╔═════════════════════════════════════════════╗\n"
        menu += "║               MENU TOURNOIS                 ║\n"
        menu += "╚═════════════════════════════════════════════╝\n"
        menu += "0. Revenir au menu tournois\n"
        print(menu)
        description = input("Entrez une description du tournoi : ")
        return description

    def ask_add_another_player(self):
        """
        Prompts the user to add more players to the tournament.

        :return: The user's response as 'o' for yes or 'n' for no.
        """
        Utils.clear_terminal()
        menu = "=" * 47 + "\n"
        menu += "         ♛ ♚ ♜ ♝ ♞ ♟ ♔ ♕ ♖ ♗ ♘ ♙ \n"
        menu += "                 EASYCHESS \n"
        menu += "=" * 47 + "\n"
        menu += "╔═════════════════════════════════════════════╗\n"
        menu += "║               MENU TOURNOIS                 ║\n"
        menu += "╚═════════════════════════════════════════════╝\n"
        menu += "0. Revenir au menu tournois\n"
        print(menu)
        input_add_another_player = input("Souhaitez-vous ajouter d'autres joueurs au tournoi ? (o/n): ")
        return input_add_another_player.lower()

    def ask_player_selection(self, players):
        """
        Prompts the user to select players to add to the tournament.

        :param players: A list of player dictionaries to choose from.
        :return: A string of selected player numbers.
        """
        menu = "=" * 47 + "\n"
        menu += "0. Revenir au menu principal\n"
        for i, player in enumerate(players, start=1):
            menu += f"{i}. {player['last_name']} {player['first_name']}\n"
        print(menu)
        selected_player_input = input(
            "Veuillez saisir le numéro des joueurs à ajouter au tournoi (séparés par des espaces) : "
        )
        return selected_player_input

    def ask_player_registration_method(self):
        """
        Prompts the user to choose a method for player registration.

        :return: The selected method as a string.
        """
        Utils.clear_terminal()
        menu = "=" * 47 + "\n"
        menu += "         ♛ ♚ ♜ ♝ ♞ ♟ ♔ ♕ ♖ ♗ ♘ ♙ \n"
        menu += "                 EASYCHESS \n"
        menu += "=" * 47 + "\n"
        menu += "╔═════════════════════════════════════════════╗\n"
        menu += "║               MENU TOURNOIS                 ║\n"
        menu += "╚═════════════════════════════════════════════╝\n"
        menu += "=" * 47 + "\n"
        menu += "0. Revenir au menu tournois\n"
        menu += "1. Importer les joueurs existant automatiquement\n"
        menu += "2. Importer les joueurs existant manuellement\n"
        menu += "3. Crée et importer un nouveau joueur\n"
        print(menu)
        method = input("Choisissez une option (0, 1, 2 ou 3) : ")
        return method

    def ask_start_tournament(self):
        """
        Prompts the user to confirm if they want to start the tournament.

        :return: The user's response as 'o' for yes or 'n' for no.
        """
        Utils.clear_terminal()
        menu = "=" * 47 + "\n"
        menu += "         ♛ ♚ ♜ ♝ ♞ ♟ ♔ ♕ ♖ ♗ ♘ ♙ \n"
        menu += "                 EASYCHESS \n"
        menu += "=" * 47 + "\n"
        menu += "╔═════════════════════════════════════════════╗\n"
        menu += "║               MENU TOURNOIS                 ║\n"
        menu += "╚═════════════════════════════════════════════╝\n"
        menu += "0. Revenir au menu tournois\n"
        print(menu)
        start_tournament_input = input("Souhaitez-vous commencer le tournoi (o/n) ? : ")
        return start_tournament_input.lower()

    def ask_return_menu(self):
        """
        Prompts the user to return to the tournament menu.

        :return: User input for returning to the menu.
        """
        menu = "=" * 47 + "\n"
        menu += "0. Revenir au menu tournois\n"
        print(menu)
        go_menu = input("Voulez vous revenir au menu tournoi ? '0' ")
        return go_menu

    def ask_validate_match(self, match, match_index):
        """
        Asks the user to validate the winner of a match.

        Returns 1 for player 1, 2 for player 2, or 0 for a draw.

        :param match: The match for which to validate the winner.
        :param match_index: The index of the match.
        :return: The user's choice (1, 2, or 0).
        """
        menu = "=" * 47 + "\n"
        menu += f"Match {match_index + 1}. {match}\n"
        menu += "=" * 47 + "\n"
        menu += f"1. {match.player1['first_name']} {match.player1['last_name']} (Joueur 1)\n"
        menu += f"2. {match.player2['first_name']} {match.player2['last_name']} (Joueur 2)\n"
        menu += "0. Match nul\n"
        menu += "=" * 47 + "\n"
        print(menu)
        user_input = input("Entrez le numéro du gagnant (1, 2 ou 0) : ")
        return user_input

    def display(self, round, round_index, num_rounds):
        """
        Clears the terminal and displays the details of the current round.

        Shows the round number, start and end times, and number of matches.

        :param round: The current round object.
        :param round_index: The index of the current round.
        :param num_rounds: The total number of rounds.
        """
        Utils.clear_terminal()
        menu = "=" * 47 + "\n"
        menu += "         ♛ ♚ ♜ ♝ ♞ ♟ ♔ ♕ ♖ ♗ ♘ ♙ \n"
        menu += "                 EASYCHESS \n"
        menu += "=" * 47 + "\n"
        menu += "╔═════════════════════════════════════════════╗\n"
        menu += "║               MENU TOURNOIS                 ║\n"
        menu += "╚═════════════════════════════════════════════╝\n"
        menu += f"Round {round_index + 1}/{num_rounds}\n"
        menu += f"Date/heure de départ: {round.start_date_time}\n"
        menu += f"Date/heure de fin: {round.end_date_time}\n"
        menu += f"Nombre de match: {len(round.matches)}\n"
        print(menu)
