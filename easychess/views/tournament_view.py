import os
import platform
import time


class TournamentView:
    def display_tournament_menu(self) -> str:
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
        self.clear_terminal()
        return choice

    def ask_name(self):
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
        self.clear_terminal()
        return name

    def ask_location(self):
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
        self.clear_terminal()
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
        self.clear_terminal()
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
        self.clear_terminal()
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
        self.clear_terminal()
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
        menu = "=" * 47 + "\n"
        menu += "0. Revenir au menu tournois\n"
        print(menu)
        go_menu = input("Voulez vous revenir au menu tournoi ? '0' ")
        return go_menu

    def ask_validate_match(self, match, match_index):
        """
        Demande à l'utilisateur de valider le gagnant du match.
        Retourne 1 pour le joueur 1, 2 pour le joueur 2, 0 pour un match nul.
        :param match: Le match pour lequel valider le gagnant.
        :return: Le choix de l'utilisateur (1, 2, ou 0)
        """
        menu = "=" * 47 + "\n"
        menu += f"Match{match_index+1}. {match}\n"
        menu += "=" * 47 + "\n"
        menu += f"1. {match.player1['first_name']} {match.player1['last_name']} (Joueur 1)\n"
        menu += f"2. {match.player2['first_name']} {match.player2['last_name']} (Joueur 2)\n"
        menu += "0. Match nul\n"
        menu += "=" * 47 + "\n"
        print(menu)
        user_input = input("Entrez le numéro du gagnant (1, 2 ou 0) : ")
        return user_input

    def display(self, round, round_index):
        menu = "=" * 47 + "\n"
        menu += "         ♛ ♚ ♜ ♝ ♞ ♟ ♔ ♕ ♖ ♗ ♘ ♙ \n"
        menu += "                 EASYCHESS \n"
        menu += "=" * 47 + "\n"
        menu += "╔═════════════════════════════════════════════╗\n"
        menu += "║               MENU TOURNOIS                 ║\n"
        menu += "╚═════════════════════════════════════════════╝\n"
        menu += f"Round {round_index + 1}\n"
        menu += f"Date/heure de départ: {round.start_date_time}\n"
        menu += f"Date/heure de fin: {round.end_date_time}\n"
        menu += f"Nombre de match: {len(round.matches)}\n"
        print(menu)

    def display_error(self, message):
        menu = "=" * 47 + "\n"
        menu += f"⚠️  ERREUR: {message}\n"
        menu += "=" * 47 + "\n"
        print(menu)
        time.sleep(1)

    def display_success(self, message):
        menu = "=" * 47 + "\n"
        menu += f"✔️  SUCCÈS: {message}\n"
        menu += "=" * 47 + "\n"
        print(menu)
        time.sleep(1)

    def clear_terminal(self):
        if platform.system() == "Windows":
            time.sleep(0.50)
            os.system("cls")

        else:
            time.sleep(0.50)
            os.system("clear")
