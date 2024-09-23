import time
from easychess.utils.utils import Utils


class PlayerView:
    def display_player_menu(self) -> str:
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
        menu = "=" * 47 + "\n"
        menu += "0. Revenir au menu principal\n"
        print(menu)
        go_menu = input("Voulez vous revenir au menu joueur ? '0' ")
        return go_menu

    def display_player_list(self, formatted_players):
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