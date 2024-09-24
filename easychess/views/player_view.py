from easychess.utils.utils import Utils


class PlayerView:
    def display_player_menu(self) -> str:
        """
        Display the player menu and return the user's choice.

        :return: The option selected by the user.
        """
        Utils.clear_terminal()
        menu = "=" * 47 + "\n"
        menu += "         ♛ ♚ ♜ ♝ ♞ ♟ ♔ ♕ ♖ ♗ ♘ ♙ \n"
        menu += "                 EASYCHESS \n"
        menu += "=" * 47 + "\n"

        menu += "╔═════════════════════════════════════════════╗\n"
        menu += "║               MENU JOUEUR                   ║\n"
        menu += "╚═════════════════════════════════════════════╝\n"
        menu += "╔═════════════════════════════════════════════╗\n"
        menu += "║  -- Actions --                              ║\n"
        menu += "║  1. Ajouter un nouveau joueur               ║\n"
        menu += "║  2. Voir liste de joueurs                   ║\n"
        menu += "║  0. Revenir au menu principale              ║\n"
        menu += "╚═════════════════════════════════════════════╝\n"
        menu += "=" * 47 + "\n"

        print(menu)

        return input(" Veuillez choisir une option : ")

    def ask_first_name(self):
        """
        Prompt the user to enter the player's first name.

        :return: The first name entered by the user.
        """
        Utils.clear_terminal()
        menu = "=" * 47 + "\n"
        menu += "         ♛ ♚ ♜ ♝ ♞ ♟ ♔ ♕ ♖ ♗ ♘ ♙ \n"
        menu += "                 EASYCHESS \n"
        menu += "=" * 47 + "\n"

        menu += "╔═════════════════════════════════════════════╗\n"
        menu += "║               MENU JOUEUR                   ║\n"
        menu += "╚═════════════════════════════════════════════╝\n"
        menu += "0. Revenir au menu principal\n"
        print(menu)
        return input("Entrez le prénom du joueur : ")

    def ask_last_name(self):
        """
        Prompt the user to enter the player's last name.

        :return: The last name entered by the user.
        """
        Utils.clear_terminal()
        menu = "=" * 47 + "\n"
        menu += "         ♛ ♚ ♜ ♝ ♞ ♟ ♔ ♕ ♖ ♗ ♘ ♙ \n"
        menu += "                 EASYCHESS \n"
        menu += "=" * 47 + "\n"

        menu += "╔═════════════════════════════════════════════╗\n"
        menu += "║               MENU JOUEUR                   ║\n"
        menu += "╚═════════════════════════════════════════════╝\n"
        menu += "0. Revenir au menu principal\n"
        print(menu)
        last_name = input("Entrez le nom du joueur : ")
        return last_name

    def ask_birthdate(self):
        """
        Prompt the user to enter the player's birthdate.

        :return: The birthdate entered by the user.
        """
        Utils.clear_terminal()
        menu = "=" * 47 + "\n"
        menu += "         ♛ ♚ ♜ ♝ ♞ ♟ ♔ ♕ ♖ ♗ ♘ ♙ \n"
        menu += "                 EASYCHESS \n"
        menu += "=" * 47 + "\n"

        menu += "╔═════════════════════════════════════════════╗\n"
        menu += "║               MENU JOUEUR                   ║\n"
        menu += "╚═════════════════════════════════════════════╝\n"
        menu += "0. Revenir au menu principal\n"
        print(menu)
        birthdate = input("Date de naissance du joueur (jj/mm/aaaa) : ")
        return birthdate

    def ask_national_id(self):
        """
        Prompt the user to enter the player's national ID.

        :return: The national ID entered by the user.
        """
        Utils.clear_terminal()
        menu = "=" * 47 + "\n"
        menu += "         ♛ ♚ ♜ ♝ ♞ ♟ ♔ ♕ ♖ ♗ ♘ ♙ \n"
        menu += "                 EASYCHESS \n"
        menu += "=" * 47 + "\n"

        menu += "╔═════════════════════════════════════════════╗\n"
        menu += "║               MENU JOUEUR                   ║\n"
        menu += "╚═════════════════════════════════════════════╝\n"
        menu += "0. Revenir au menu principal\n"
        print(menu)
        national_id = input("Entrez le N° d'identité nationale du joueur : ")
        return national_id

    def ask_return_menu(self):
        """
        Ask the user if they want to return to the player menu.

        :return: The user's response indicating whether to return to the menu.
        """
        menu = "=" * 47 + "\n"
        menu += "0. Revenir au menu principal\n"
        print(menu)
        go_menu = input("Voulez vous revenir au menu joueur ? '0' ")
        return go_menu

    def display_player_list(self, formatted_players):
        """
        Display the list of players.

        :param formatted_players: A string representing the formatted list of players.
        """
        Utils.clear_terminal()
        menu = "=" * 47 + "\n"
        menu += "         ♛ ♚ ♜ ♝ ♞ ♟ ♔ ♕ ♖ ♗ ♘ ♙ \n"
        menu += "                 EASYCHESS \n"
        menu += "=" * 47 + "\n"

        menu += "╔═════════════════════════════════════════════╗\n"
        menu += "║               MENU JOUEUR                   ║\n"
        menu += "╚═════════════════════════════════════════════╝\n"
        menu += "0. Revenir au menu principal\n"
        menu += f"({len(formatted_players)} joueurs), présent dans la base de données : \n"
        menu += formatted_players
        print(menu)
