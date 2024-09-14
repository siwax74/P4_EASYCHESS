import time


class PlayerView:
    def display_player_menu(self) -> str:
        menu = "=" * 47 + "\n"
        menu += "         ♛ ♚ ♜ ♝ ♞ ♟ ♔ ♕ ♖ ♗ ♘ ♙ \n"
        menu += "                 EASYCHESS \n"
        menu += "=" * 47 + "\n"

        menu += "╔════════════════════════════════════════════╗\n"
        menu += "║               MENU JOUEUR                  ║\n"
        menu += "╚════════════════════════════════════════════╝\n"
        menu += "╔════════════════════════════════════════════╗\n"
        menu += "║  -- Actions --                             ║\n"
        menu += "║  0. Revenir au menu principale             ║\n"
        menu += "║  1. Ajouter un nouveau joueur              ║\n"
        menu += "║  2. Voir liste de joueurs                  ║\n"
        menu += "╚════════════════════════════════════════════╝\n"
        menu += "=" * 47 + "\n"

        print(menu)

        return input(" Veuillez choisir une option : ")

    def ask_first_name(self):
        menu = "=" * 47 + "\n"
        menu += "0. Revenir au menu principal\n"
        print(menu)
        return input("Entrez le prénom du joueur : ")

    def ask_last_name(self):
        menu = "=" * 47 + "\n"
        menu += "0. Revenir au menu principal\n"
        print(menu)
        last_name = input("Entrez le nom du joueur : ")
        return last_name

    def ask_birthdate(self):
        menu = "=" * 47 + "\n"
        menu += "0. Revenir au menu principal\n"
        print(menu)
        birthdate = input("Date de naissance du joueur (jj/mm/aaaa) : ")
        return birthdate

    def ask_national_id(self):
        menu = "=" * 47 + "\n"
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
        menu = "=" * 47 + "\n"
        menu += "      --- Liste des joueurs ---      \n"
        menu += "=" * 47 + "\n"
        menu += f"({len(formatted_players)} joueurs), présent dans la base de données : \n"
        menu += formatted_players
        print(menu)

    def display_error(self, message):
        menu = "=" * 47 + "\n"
        menu += f"⚠️  ERREUR: {message}\n"
        menu += "=" * 47 + "\n"
        print(menu)
        time.sleep(2)

    def display_success(self, message):
        menu = "=" * 47 + "\n"
        menu += f"✔️  SUCCÈS: {message}\n"
        menu += "=" * 47 + "\n"
        print(menu)
        time.sleep(2)
