from easychess.utils.utils import Utils


class PlayerView:
    def display_player_menu(self) -> str:
        """
        Clears the terminal and displays the player menu.

        This menu allows the user to choose actions related to player management,
        including adding a new player or viewing the list of players.

        :return: The user's choice as a string.
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
        menu += "║  0. Revenir au menu principale              ║\n"
        menu += "║  1. Ajouter un nouveau joueur               ║\n"
        menu += "║  2. Voir liste de joueurs                   ║\n"
        menu += "╚═════════════════════════════════════════════╝\n"
        menu += "=" * 47 + "\n"

        print(menu)

        return input(" Veuillez choisir une option : ")

    def ask_first_name(self):
        """
        Clears the terminal and prompts the user for the player's first name.

        :return: The first name of the player as a string.
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
        Clears the terminal and prompts the user for the player's last name.

        :return: The last name of the player as a string.
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
        Clears the terminal and prompts the user for the player's birthdate.

        :return: The birthdate of the player as a string.
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
        Clears the terminal and prompts the user for the player's national ID.

        :return: The national ID of the player as a string.
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
        Displays a prompt asking the user if they want to return to the player menu.

        :return: User's choice as a string.
        """
        menu = "=" * 47 + "\n"
        menu += "0. Revenir au menu principal\n"
        print(menu)
        go_menu = input("Voulez vous revenir au menu joueur ? '0' ")
        return go_menu

    def display_player_list(self, formatted_players):
        """
        Clears the terminal and displays the list of players.

        This method formats and prints the player list along with a count of players.

        :param formatted_players: A string representation of the players' list.
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
